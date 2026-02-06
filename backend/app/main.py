# main.py
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional, List
from contextlib import asynccontextmanager
import os
import hashlib
from .schemas import OpportunityCreate
from fastapi import FastAPI, Depends, HTTPException, status, Header, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
import bcrypt
from fastapi import BackgroundTasks
import json
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update
from .models import engine, async_session, Base, User, Opportunity, SavedOpportunity, Application, Report, RateLimit, ModerationLinkOpen
import re
import string
import json
from urllib.parse import urlparse
from . import url_safety

from .schemas import (
    UserCreate,
    UserOut,
    Token,
    LoginByEmail,
    OpportunityOut,
    DashboardOut,
    DashboardStats,
    ApplicationCreate,
    ApplicationOut,
    ApplicationInboxItem,
    ApplicationInboxOut,
    OpportunityUpdate, MyOpportunityOut, ApplicationDecisionIn, MyApplicationItem, ReportCreate,
    AppealCreate, AppealDecision, AppealItem, ReportedOpportunityItem, ReportItem, ReportDecision,
    ExternalUrlItem, ExternalUrlDecision, ContactCreate,
    LinkInfoOut, OpenInSandboxAction, OpenInSandboxOut,
)
from openai import OpenAI
import anyio
from functools import lru_cache

from dotenv import load_dotenv
load_dotenv()
# =========================
# Config
# =========================
SECRET_KEY = os.environ.get("SECRET_KEY", "dev_only_change_me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
MODERATOR_EMAILS = {e.strip().lower() for e in os.environ.get("MODERATOR_EMAILS", "").split(",") if e.strip()}
def require_moderator(user: User) -> None:
    # If MODERATOR_EMAILS is empty, lock moderation down (nobody is moderator)
    if not MODERATOR_EMAILS:
        raise HTTPException(
            status_code=403,
            detail={"code": "FORBIDDEN", "message": "Moderator access is not configured. MODERATOR_EMAILS environment variable is not set or empty."},
        )

    user_email_normalized = (user.email or "").strip().lower()
    if user_email_normalized not in MODERATOR_EMAILS:
        raise HTTPException(
            status_code=403,
            detail={
                "code": "FORBIDDEN", 
                "message": f"Moderator only. Your email ({user.email}) is not in the moderator list.",
                "user_email": user.email,
                "moderator_emails_count": len(MODERATOR_EMAILS)
            },
        )


WWW_AUTH = {"WWW-Authenticate": "Bearer"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

# CORS configuration - allow frontend origins from environment or default to localhost
FRONTEND_URLS = os.environ.get("FRONTEND_URLS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
FRONTEND_URLS = [url.strip() for url in FRONTEND_URLS if url.strip()]

# Add Vercel pattern to allow any Vercel deployment (production, preview, etc.)
# This regex matches: https://*.vercel.app (with or without trailing slash)
VERCEL_PATTERN = r"https://.*\.vercel\.app$"

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_URLS,
    allow_origin_regex=VERCEL_PATTERN,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Explicit OPTIONS handler as fallback
@app.options("/{full_path:path}")
async def options_handler(full_path: str, origin: Optional[str] = Header(None)):
    """Handle OPTIONS requests explicitly - CORS preflight"""
    from fastapi.responses import Response
    import re
    
    # Check if origin matches allowed patterns
    allowed = False
    if origin:
        # Check against explicit URLs
        if origin in FRONTEND_URLS:
            allowed = True
        # Check against Vercel regex
        elif re.match(VERCEL_PATTERN, origin):
            allowed = True
    
    if not allowed:
        return Response(status_code=400)
    
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": origin if origin else FRONTEND_URLS[0] if FRONTEND_URLS else "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "3600",
        }
    )

# =========================
# DB dependency (async)
# =========================
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

DbDep = Annotated[AsyncSession, Depends(get_db)]

# =========================
# Password helpers
# =========================
def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        sha256_hash = hashlib.sha256(password_bytes).hexdigest()
        return bcrypt.hashpw(sha256_hash.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    plain_bytes = plain.encode("utf-8")
    hashed_bytes = hashed.encode("utf-8")
    if len(plain_bytes) > 72:
        sha256_hash = hashlib.sha256(plain_bytes).hexdigest()
        return bcrypt.checkpw(sha256_hash.encode("utf-8"), hashed_bytes)
    return bcrypt.checkpw(plain_bytes, hashed_bytes)

def create_access_token_for_user_id(user_id: int, minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> tuple[str, int]:
    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    to_encode = {"sub": str(user_id), "exp": expire}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token, minutes * 60

# =========================
# User fetch helpers
# =========================
async def get_user_by_username(db: DbDep, username: str) -> Optional[User]:
    res = await db.execute(select(User).where(User.username == username))
    return res.scalar_one_or_none()

async def get_user_by_email(db: DbDep, email: str) -> Optional[User]:
    res = await db.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()

async def get_user_by_id(db: DbDep, user_id: int) -> Optional[User]:
    res = await db.execute(select(User).where(User.id == user_id))
    return res.scalar_one_or_none()

# =========================
# Auth dependency (Bearer)
# =========================
async def get_bearer_token(authorization: Optional[str] = Header(None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header", headers=WWW_AUTH)

    parts = authorization.strip().split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization scheme", headers=WWW_AUTH)

    token = parts[1].strip()
    if not token:
        raise HTTPException(status_code=401, detail="Empty bearer token", headers=WWW_AUTH)
    return token

async def get_current_user(db: DbDep, token: Annotated[str, Depends(get_bearer_token)]) -> User:
    invalid = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers=WWW_AUTH)
    expired = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired", headers=WWW_AUTH)

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_aud": False, "leeway": 10},
        )
        sub = payload.get("sub")
        if not sub:
            raise invalid
        user_id = int(sub)
    except ExpiredSignatureError:
        raise expired
    except (JWTError, ValueError):
        raise invalid

    user = await get_user_by_id(db, user_id)
    if not user:
        raise invalid
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

# =========================
# Small utils
# =========================
def csv_to_tags(csv: str) -> list[str]:
    return [t.strip() for t in (csv or "").split(",") if t.strip()]

def tags_to_csv(tags: list[str]) -> str:
    return ",".join([t.strip() for t in (tags or []) if t.strip()])


def opp_to_out(opp: Opportunity, saved: bool) -> OpportunityOut:
    return OpportunityOut(
        id=opp.id,
        type=opp.type,
        title=opp.title,
        org=opp.org,
        description=opp.description,
        location=opp.location,

        deadline_at=opp.deadline_at,
        deadline_text=opp.deadline_text or "",

        tags=csv_to_tags(opp.tags_csv),
        saved=saved,
        contact_email=opp.contact_email,
        allow_apply=opp.allow_apply,
        allow_external_apply=opp.allow_external_apply,
        external_apply_url=opp.external_apply_url,
        external_url_approved=opp.external_url_approved,
    )


def app_to_out(a: Application) -> ApplicationOut:
    return ApplicationOut(
        id=a.id,
        opportunity_id=a.opportunity_id,
        applicant_user_id=a.applicant_user_id,
        full_name=a.full_name,
        email=a.email,
        message=a.message,
        created_at=a.created_at,
        status=a.status,
        decision_reason=a.decision_reason,
        decided_at=a.decided_at,
        decided_by_user_id=a.decided_by_user_id,
    )

def as_utc(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    # naive -> assume UTC
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        return dt.replace(tzinfo=timezone.utc)
    # aware -> convert to UTC
    return dt.astimezone(timezone.utc)


# =========================
# Spam Protection Helpers
# =========================

# Rate limit configuration: action -> (max_count, window_seconds)
RATE_LIMITS = {
    "create_opportunity": (5, 3600),   # 5 per hour
    "update_opportunity": (20, 3600),  # 20 per hour
}


def normalize_text(text: str) -> str:
    """Normalize text: lowercase, trim, collapse whitespace, remove punctuation."""
    if not text:
        return ""
    text = text.lower().strip()
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def opportunity_hash(
    user_id: int,
    title: str,
    org: str,
    description: str,
    location: str,
    tags: list[str],
) -> str:
    """
    Compute sha256 hash of normalized opportunity content.
    Used for duplicate detection.
    """
    normalized_tags = sorted([normalize_text(t) for t in (tags or []) if t.strip()])
    parts = [
        str(user_id),
        normalize_text(title),
        normalize_text(org),
        normalize_text(description),
        normalize_text(location),
        ",".join(normalized_tags),
    ]
    combined = "|".join(parts)
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()


async def enforce_rate_limit(
    db: AsyncSession,
    user_id: int,
    action: str,
) -> None:
    """
    Check and enforce rate limit for a user action.
    Raises HTTPException 429 if limit exceeded.
    """
    if action not in RATE_LIMITS:
        return  # No limit configured for this action

    max_count, window_seconds = RATE_LIMITS[action]
    now = datetime.now(timezone.utc)

    # Try to get existing rate limit record
    result = await db.execute(
        select(RateLimit).where(
            RateLimit.user_id == user_id,
            RateLimit.action == action,
        )
    )
    rate_limit = result.scalar_one_or_none()

    if rate_limit is None:
        # First request for this action - create new record
        rate_limit = RateLimit(
            user_id=user_id,
            action=action,
            window_start=now,
            count=1,
        )
        db.add(rate_limit)
        await db.commit()
        return

    # Check if window has expired
    # Ensure window_start is timezone-aware (some databases may return naive datetimes)
    window_start = rate_limit.window_start
    if window_start.tzinfo is None:
        window_start = window_start.replace(tzinfo=timezone.utc)
    window_end = window_start + timedelta(seconds=window_seconds)

    if now >= window_end:
        # Window expired - reset
        rate_limit.window_start = now
        rate_limit.count = 1
        await db.commit()
        return

    # Window still active - check count
    if rate_limit.count >= max_count:
        # Rate limit exceeded
        retry_after = int((window_end - now).total_seconds())
        if retry_after < 1:
            retry_after = 1

        print(f"[RATE_LIMIT] user={user_id} action={action} retry_after={retry_after}s")

        raise HTTPException(
            status_code=429,
            detail={
                "code": "RATE_LIMITED",
                "message": f"Too many requests. Please wait {retry_after} seconds.",
                "retry_after_seconds": retry_after,
            },
        )

    # Increment count
    rate_limit.count += 1
    await db.commit()


# =========================
# AI moderation
# =========================
# =========================
# AI moderation
# =========================
@lru_cache(maxsize=1)
def _openai_client() -> OpenAI:
    # Reads OPENAI_API_KEY from environment automatically
    return OpenAI()

def _build_opportunity_text(payload) -> str:
    parts = [
        f"type: {payload.type or ''}",
        f"title: {payload.title or ''}",
        f"org: {payload.org or ''}",
        f"description: {payload.description or ''}",
        f"location: {payload.location or ''}",
        f"deadline_text: {payload.deadline_text or ''}",
        f"contact_email: {str(payload.contact_email) if getattr(payload, 'contact_email', None) else ''}",
        f"external_apply_url: {payload.external_apply_url or ''}",
        f"tags: {', '.join(payload.tags or [])}",
    ]
    return "\n".join(p.strip() for p in parts if p and p.strip())

def _moderate_text_sync(text: str) -> dict:
    """
    Returns:
      {
        flagged: bool,
        categories: dict[str, bool],
        category_scores: dict[str, float]
      }
    """
    client = _openai_client()
    resp = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    r = resp.results[0]
    return {
        "flagged": bool(r.flagged),
        "categories": dict(r.categories),
        "category_scores": dict(r.category_scores),
    }

async def moderate_opportunity_payload(payload) -> dict:
    text = _build_opportunity_text(payload).strip()
    if not text:
        return {"flagged": False, "categories": {}, "category_scores": {}}

    # SDK call is sync; run in a thread so FastAPI stays responsive
    return await anyio.to_thread.run_sync(_moderate_text_sync, text)
async def moderate_opportunity_after_create(opportunity_id: int, payload_dict: dict):
    async with async_session() as session:
        try:
            # load current state
            opp = (await session.execute(
                select(Opportunity).where(Opportunity.id == opportunity_id)
            )).scalar_one_or_none()
            if opp is None:
                return

            # If a moderator already flagged it (external URL rejection / reports), don't override
            if opp.is_flagged and opp.flagged_reason and opp.flagged_reason != "Auto-flagged by AI moderation":
                return

            # build temp payload
            class _TempPayload:
                type = payload_dict.get("type")
                title = payload_dict.get("title")
                org = payload_dict.get("org")
                description = payload_dict.get("description")
                location = payload_dict.get("location")
                deadline_text = payload_dict.get("deadline_text")
                contact_email = payload_dict.get("contact_email")
                external_apply_url = payload_dict.get("external_apply_url")
                tags = payload_dict.get("tags")

            mod = await moderate_opportunity_payload(_TempPayload)
            is_flagged = bool(mod.get("flagged"))
            categories = mod.get("categories") or {}
            true_cats = [k for k, v in categories.items() if v]

            # Only write AI fields
            opp.is_flagged = is_flagged
            opp.flagged_at = datetime.now(timezone.utc) if is_flagged else None
            opp.flagged_reason = "Auto-flagged by AI moderation" if is_flagged else None
            opp.flagged_categories = json.dumps(true_cats) if true_cats else None

            await session.commit()

        except Exception as e:
            print(f"[moderation background] failed for opp_id={opportunity_id}: {e}")
            await session.rollback()


# =========================
# Root + Health (avoid 405 on GET / from Render/browsers)
# =========================
@app.get("/")
async def root():
    return {"message": "Opportunity Hub API", "docs": "/docs", "health": "/health"}


@app.get("/health")
async def health():
    return {"status": "ok"}

# =========================
# Auth routes
# =========================
@app.post("/register", response_model=Token, status_code=201)
async def register(user: UserCreate, db: DbDep):
    email_norm = user.email.strip().lower()

    if await get_user_by_username(db, user.username):
        raise HTTPException(status_code=409, detail={"code": "USERNAME_TAKEN", "message": "Username already taken."})
    if await get_user_by_email(db, email_norm):
        raise HTTPException(status_code=409, detail={"code": "EMAIL_TAKEN", "message": "Email already registered."})

    password_hash = hash_password(user.password)

    db_user = User(username=user.username, email=email_norm, password_hash=password_hash)
    db.add(db_user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail={"code": "UNIQUE_CONFLICT", "message": "Username or email already registered."})
    await db.refresh(db_user)

    access_token, expires_in = create_access_token_for_user_id(db_user.id)
    return {"access_token": access_token, "token_type": "bearer", "expires_in": expires_in}

@app.post("/auth/login", response_model=Token)
async def login(payload: LoginByEmail, db: DbDep):
    email_norm = payload.email.strip().lower()
    user = await get_user_by_email(db, email_norm)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail={"code": "INVALID_CREDENTIALS", "message": "Incorrect email or password"},
            headers=WWW_AUTH,
        )

    access_token, expires_in = create_access_token_for_user_id(user.id)
    return {"access_token": access_token, "token_type": "bearer", "expires_in": expires_in}


@app.get("/users/me", response_model=UserOut)
async def read_users_me(current_user: CurrentUser):
    return UserOut(id=current_user.id, username=current_user.username, email=current_user.email)

@app.get("/moderation/check")
async def check_moderator_status(current_user: CurrentUser):
    """Debug endpoint to check moderator status - helps troubleshoot moderator access issues."""
    user_email_lower = (current_user.email or "").strip().lower()
    is_configured = bool(MODERATOR_EMAILS)
    is_moderator = user_email_lower in MODERATOR_EMAILS
    
    return {
        "user_email": current_user.email,
        "user_email_normalized": user_email_lower,
        "moderator_emails_configured": is_configured,
        "moderator_emails_count": len(MODERATOR_EMAILS),
        "is_moderator": is_moderator,
        "configured_emails": list(MODERATOR_EMAILS) if is_moderator else []  # Only show if already a moderator
    }

# =========================
# Opportunities + Saved
# =========================

@app.get("/opportunities", response_model=list[OpportunityOut])
async def list_opportunities(
    db: DbDep,
    current_user: CurrentUser,
    type: Optional[str] = Query(default=None, description="internship/club/volunteering/tutor"),
    q: Optional[str] = Query(default=None, description="search in title/org/description"),
):
    # Hide posts with pending or rejected external URL
    # Show posts where:
    # - Never had external apply (external_url_approved is NULL and allow_external_apply is False)
    # - External URL was approved
    stmt = (
        select(Opportunity)
        .where(Opportunity.is_flagged == False)
        .where(
            ((Opportunity.external_url_approved.is_(None)) & (Opportunity.allow_external_apply == False)) |
            (Opportunity.external_url_approved == True)
        )
        .order_by(Opportunity.created_at.desc())
    )


    if type:
        stmt = stmt.where(Opportunity.type == type.strip().lower())

    if q:
        like = f"%{q.strip()}%"
        stmt = stmt.where(
            Opportunity.title.ilike(like) |
            Opportunity.org.ilike(like) |
            Opportunity.description.ilike(like)
        )

    opps = (await db.execute(stmt)).scalars().all()

    # Fetch saved ids for this user in one query
    saved_rows = (await db.execute(
        select(SavedOpportunity.opportunity_id).where(SavedOpportunity.user_id == current_user.id)
    )).all()
    saved_ids = {row[0] for row in saved_rows}

    return [opp_to_out(o, o.id in saved_ids) for o in opps]


@app.post("/opportunities/{opportunity_id}/save", status_code=204)
async def save_opportunity(opportunity_id: int, db: DbDep, current_user: CurrentUser):
    opp = await db.get(Opportunity, opportunity_id)
    if not opp:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Opportunity not found"})

    # insert join row (unique constraint prevents duplicates)
    db.add(SavedOpportunity(user_id=current_user.id, opportunity_id=opportunity_id))
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        # already saved - treat as success
    return None


@app.delete("/opportunities/{opportunity_id}/save", status_code=204)
async def unsave_opportunity(opportunity_id: int, db: DbDep, current_user: CurrentUser):
    await db.execute(
        delete(SavedOpportunity).where(
            SavedOpportunity.user_id == current_user.id,
            SavedOpportunity.opportunity_id == opportunity_id,
        )
    )
    await db.commit()
    return None



@app.get("/users/me/saved", response_model=list[OpportunityOut])
async def list_saved(db: DbDep, current_user: CurrentUser):
    stmt = (
        select(Opportunity)
        .join(SavedOpportunity, SavedOpportunity.opportunity_id == Opportunity.id)
        .where(SavedOpportunity.user_id == current_user.id)
        .order_by(SavedOpportunity.created_at.desc())
    )
    opps = (await db.execute(stmt)).scalars().all()
    return [opp_to_out(o, True) for o in opps]


@app.get("/dashboard", response_model=DashboardOut)
async def dashboard(db: DbDep, current_user: CurrentUser):
    # trending: just newest items for now
    # Hide posts with pending or rejected external URL
    opps = (await db.execute(
        select(Opportunity)
        .where(Opportunity.is_flagged == False)
        .where(
            ((Opportunity.external_url_approved.is_(None)) & (Opportunity.allow_external_apply == False)) |
            (Opportunity.external_url_approved == True)
        )
        .order_by(Opportunity.created_at.desc())
    )).scalars().all()


    saved_opps = (await db.execute(
        select(Opportunity)
        .join(SavedOpportunity, SavedOpportunity.opportunity_id == Opportunity.id)
        .where(SavedOpportunity.user_id == current_user.id)
        .order_by(SavedOpportunity.created_at.desc())
    )).scalars().all()

    saved_ids = {o.id for o in saved_opps}
    trending_out = [opp_to_out(o, o.id in saved_ids) for o in opps]
    saved_out = [opp_to_out(o, True) for o in saved_opps]
    apps_count = (await db.execute(
    select(func.count(Application.id)).where(Application.applicant_user_id == current_user.id)
    )).scalar_one()

    stats = DashboardStats(
        newMatches=len(trending_out),
        saved=len(saved_out),
        applications=apps_count,
        )


    me = UserOut(id=current_user.id, username=current_user.username, email=current_user.email)
    return DashboardOut(me=me, stats=stats, trending=trending_out, saved=saved_out)
    

@app.post("/opportunities", response_model=OpportunityOut, status_code=201)
async def create_opportunity(
    payload: OpportunityCreate,
    db: DbDep,
    current_user: CurrentUser,
    background_tasks: BackgroundTasks,
):
    # 1) Honeypot
    if payload.website and payload.website.strip():
        raise HTTPException(status_code=400, detail={"code": "INVALID", "message": "Invalid request"})

    # 2) Rate limiting
    await enforce_rate_limit(db, current_user.id, "create_opportunity")

    # 3) Duplicate detection (same as yours)
    content_hash = opportunity_hash(
        user_id=current_user.id,
        title=payload.title,
        org=payload.org,
        description=payload.description,
        location=payload.location,
        tags=payload.tags,
    )

    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    dup_result = await db.execute(
        select(Opportunity).where(
            Opportunity.creator_user_id == current_user.id,
            Opportunity.content_hash == content_hash,
            Opportunity.created_at >= cutoff,
        )
    )
    if dup_result.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail={"code": "DUPLICATE", "message": "Duplicate opportunity (same content recently)."})

    deadline_at = payload.deadline_at
    if deadline_at is not None and (deadline_at.tzinfo is None or deadline_at.tzinfo.utcoffset(deadline_at) is None):
        deadline_at = deadline_at.replace(tzinfo=timezone.utc)

    # 4) Create quickly (no moderation blocking)
    opp = Opportunity(
        creator_user_id=current_user.id,
        type=payload.type.strip().lower(),
        title=payload.title.strip(),
        org=payload.org.strip(),
        description=payload.description.strip(),
        location=payload.location.strip(),
        tags_csv=tags_to_csv(payload.tags),

        deadline_at=deadline_at,
        deadline_text=(payload.deadline_text or "").strip(),

        contact_email=str(payload.contact_email).strip().lower(),
        allow_apply=bool(payload.allow_apply),
        allow_external_apply=bool(payload.allow_external_apply),
        external_apply_url=(payload.external_apply_url.strip() if payload.external_apply_url else None),

        # External URLs need moderator approval (None = pending)
        external_url_approved=(None if payload.allow_external_apply and payload.external_apply_url else None),

        # moderation fields initially empty/clean
        is_flagged=False,
        flagged_categories=None,
        flagged_at=None,
        flagged_reason=None,

        content_hash=content_hash,
    )

    db.add(opp)
    await db.commit()
    await db.refresh(opp)

    # 5) Run moderation later (background)
    # Pass only simple data, not the db session
    background_tasks.add_task(
        moderate_opportunity_after_create,
        opp.id,
        {
            "type": payload.type,
            "title": payload.title,
            "org": payload.org,
            "description": payload.description,
            "location": payload.location,
            "deadline_text": payload.deadline_text,
            "contact_email": str(payload.contact_email),
            "external_apply_url": payload.external_apply_url,
            "tags": payload.tags,
        },
    )

    return opp_to_out(opp, saved=False)



@app.get("/users/me/opportunities", response_model=list[MyOpportunityOut])
async def my_opportunities(
    db: DbDep,
    current_user: CurrentUser,
    type: Optional[str] = Query(default=None, description="internship/club/volunteering/tutor"),
    q: Optional[str] = Query(default=None, description="search in title/org/description"),
):
    stmt = (
        select(Opportunity)
        .where(Opportunity.creator_user_id == current_user.id)
        .order_by(Opportunity.created_at.desc())
    )

    if type:
        stmt = stmt.where(Opportunity.type == type.strip().lower())

    if q:
        like = f"%{q.strip()}%"
        stmt = stmt.where(
            Opportunity.title.ilike(like) |
            Opportunity.org.ilike(like) |
            Opportunity.description.ilike(like)
        )

    # 1) fetch opps first
    opps = (await db.execute(stmt)).scalars().all()

    # 2) saved ids
    saved_rows = (await db.execute(
        select(SavedOpportunity.opportunity_id).where(SavedOpportunity.user_id == current_user.id)
    )).all()
    saved_ids = {r[0] for r in saved_rows}

    # 3) count apps per opp (only if opps exist)
    counts: dict[int, int] = {}
    if opps:
        counts_rows = (await db.execute(
            select(Application.opportunity_id, func.count(Application.id))
            .where(Application.opportunity_id.in_([o.id for o in opps]))
            .group_by(Application.opportunity_id)
        )).all()
        counts = {oid: c for (oid, c) in counts_rows}

    # 4) build output
    out: list[MyOpportunityOut] = []
    for o in opps:
        base = opp_to_out(o, o.id in saved_ids).model_dump()
        out.append(MyOpportunityOut(
            **base,
            applications_count=counts.get(o.id, 0),
            is_flagged=o.is_flagged,
            flagged_reason=o.flagged_reason,
            flagged_at=o.flagged_at,
            flagged_categories=(json.loads(o.flagged_categories) if o.flagged_categories else []),
            # Appeal fields
            appeal_message=o.appeal_message,
            appeal_at=o.appeal_at,
            appeal_status=o.appeal_status,
            appeal_response=o.appeal_response,
            appeal_decided_at=o.appeal_decided_at,
        ))


    return out



@app.delete("/opportunities/{opportunity_id}", status_code=204)
async def delete_my_opportunity(
    opportunity_id: int,
    db: DbDep,
    current_user: CurrentUser,
):
    # 1) Fetch by ID only
    result = await db.execute(
        select(Opportunity).where(Opportunity.id == opportunity_id)
    )
    opp = result.scalar_one_or_none()

    # 2) Not found
    if opp is None:
        raise HTTPException(
            status_code=404,
            detail={"code": "NOT_FOUND", "message": "Opportunity not found"},
        )

    # 3) Exists but not owned by user
    if opp.creator_user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail={"code": "FORBIDDEN", "message": "You are not the creator of this opportunity"},
        )

    # 4) Delete dependent rows first
    await db.execute(
        delete(SavedOpportunity).where(
            SavedOpportunity.opportunity_id == opportunity_id
        )
    )

    # 5) Delete the opportunity
    await db.execute(
        delete(Opportunity).where(Opportunity.id == opportunity_id)
    )

    # 6) Commit
    await db.commit()
    return None


@app.post("/opportunities/{opportunity_id}/apply", response_model=ApplicationOut, status_code=201)
async def apply_to_opportunity(
    opportunity_id: int,
    payload: ApplicationCreate,
    db: DbDep,
    current_user: CurrentUser,
):
    # 1) find opportunity
    res = await db.execute(select(Opportunity).where(Opportunity.id == opportunity_id))
    opp = res.scalar_one_or_none()
    if opp is None:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Opportunity not found"})

    # 2) check apply enabled
    if not opp.allow_apply:
        raise HTTPException(status_code=400, detail={"code": "APPLY_DISABLED", "message": "Applications are disabled for this post"})
    # deadline guard (auto-close)
    # deadline guard (auto-close)
    if opp.deadline_at is not None:
        now = datetime.now(timezone.utc)
        deadline = as_utc(opp.deadline_at)

        if deadline is not None and now > deadline:
                raise HTTPException(status_code=400, detail={"code":"DEADLINE_PASSED","message":"Deadline has passed"})


    # 3) create application
    a = Application(
    opportunity_id=opportunity_id,
    applicant_user_id=current_user.id,
    full_name=payload.full_name.strip(),
    email=str(payload.email).strip().lower(),
    message=(payload.message or "").strip(),
    status="pending",
    decision_reason=None,
    decided_at=None,
    decided_by_user_id=None,
    )

    db.add(a)

    # 4) commit (handle duplicate apply)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail={"code": "ALREADY_APPLIED", "message": "You already applied to this opportunity"})

    await db.refresh(a)
    return app_to_out(a)


@app.get("/opportunities/{opportunity_id}/applications", response_model=list[ApplicationOut])
async def list_applications_for_opportunity(
    opportunity_id: int,
    db: DbDep,
    current_user: CurrentUser,
):
    # 1) load opportunity
    res = await db.execute(select(Opportunity).where(Opportunity.id == opportunity_id))
    opp = res.scalar_one_or_none()
    if opp is None:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Opportunity not found"})

    # 2) owner check
    if opp.creator_user_id != current_user.id:
        raise HTTPException(status_code=403, detail={"code": "FORBIDDEN", "message": "Not your opportunity"})

    # 3) fetch applications
    apps = (await db.execute(
        select(Application)
        .where(Application.opportunity_id == opportunity_id)
        .order_by(Application.created_at.desc())
    )).scalars().all()

    return [app_to_out(a) for a in apps]

@app.get("/users/me/application-inbox", response_model=ApplicationInboxOut)
async def application_inbox(db: DbDep, current_user: CurrentUser):
    stmt = (
        select(
            Opportunity.id.label("opportunity_id"),
            Opportunity.title,
            Opportunity.org,
            Opportunity.type,
            func.count(Application.id).label("applications_count"),
            func.max(Application.created_at).label("latest_application_at"),
        )
        .join(Application, Application.opportunity_id == Opportunity.id, isouter=True)
        .where(Opportunity.creator_user_id == current_user.id)
        .group_by(Opportunity.id)
        .order_by(func.max(Application.created_at).desc().nullslast(), Opportunity.created_at.desc())
    )

    rows = (await db.execute(stmt)).all()

    items = [
        ApplicationInboxItem(
            opportunity_id=r.opportunity_id,
            title=r.title,
            org=r.org,
            type=r.type,
            applications_count=r.applications_count,
            latest_application_at=r.latest_application_at,
        )
        for r in rows
    ]

    return ApplicationInboxOut(items=items)

@app.get("/users/me/applications", response_model=list[MyApplicationItem])
async def my_applications(db: DbDep, current_user: CurrentUser):
    rows = (await db.execute(
        select(Application, Opportunity)
        .join(Opportunity, Opportunity.id == Application.opportunity_id)
        .where(Application.applicant_user_id == current_user.id)
        .order_by(Application.created_at.desc())
    )).all()

    # need saved status for each opp for consistency (optional)
    saved_rows = (await db.execute(
        select(SavedOpportunity.opportunity_id).where(SavedOpportunity.user_id == current_user.id)
    )).all()
    saved_ids = {r[0] for r in saved_rows}

    out = []
    for a, o in rows:
        out.append({
            "application": app_to_out(a),
            "opportunity": opp_to_out(o, o.id in saved_ids)
        })
    return out

@app.patch("/opportunities/{opportunity_id}/applications/{application_id}", response_model=ApplicationOut)
async def decide_application(
    opportunity_id: int,
    application_id: int,
    payload: ApplicationDecisionIn,
    db: DbDep,
    current_user: CurrentUser,
):
    # load opportunity
    opp = (await db.execute(select(Opportunity).where(Opportunity.id == opportunity_id))).scalar_one_or_none()
    if opp is None:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Opportunity not found"})

    # creator-only
    if opp.creator_user_id != current_user.id:
        raise HTTPException(status_code=403, detail={"code": "FORBIDDEN", "message": "Not your opportunity"})

    # load application
    app = (await db.execute(
        select(Application).where(
            Application.id == application_id,
            Application.opportunity_id == opportunity_id,
        )
    )).scalar_one_or_none()

    if app is None:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Application not found"})

    # apply decision
    app.status = payload.status
    reason = (payload.reason or "").strip()
    app.decision_reason = reason if (payload.status == "rejected" and reason) else (reason or None)

    app.decided_at = datetime.now(timezone.utc)
    app.decided_by_user_id = current_user.id

    await db.commit()
    await db.refresh(app)
    return app_to_out(app)


@app.patch("/opportunities/{opportunity_id}", response_model=OpportunityOut)
async def update_my_opportunity(
    opportunity_id: int,
    payload: OpportunityUpdate,
    db: DbDep,
    current_user: CurrentUser,
):
    # --- Rate limiting ---
    await enforce_rate_limit(db, current_user.id, "update_opportunity")

    opp = (await db.execute(
        select(Opportunity).where(Opportunity.id == opportunity_id)
    )).scalar_one_or_none()

    if opp is None:
        raise HTTPException(
            status_code=404,
            detail={"code": "NOT_FOUND", "message": "Opportunity not found"},
        )

    if opp.creator_user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail={"code": "FORBIDDEN", "message": "You are not the creator"},
        )

    # -------------------------
    # Apply updates (partial-safe)
    # -------------------------
    if payload.type is not None:
        opp.type = payload.type.strip().lower()
    if payload.title is not None:
        opp.title = payload.title.strip()
    if payload.org is not None:
        opp.org = payload.org.strip()
    if payload.description is not None:
        opp.description = payload.description.strip()
    if payload.location is not None:
        opp.location = payload.location.strip()

    if "deadline_at" in payload.model_fields_set:
        dt = payload.deadline_at
        if dt is not None and (dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None):
            dt = dt.replace(tzinfo=timezone.utc)
        opp.deadline_at = dt

    if "deadline_text" in payload.model_fields_set:
        opp.deadline_text = (payload.deadline_text or "").strip()

    if payload.tags is not None:
        opp.tags_csv = tags_to_csv(payload.tags)

    if payload.contact_email is not None:
        opp.contact_email = str(payload.contact_email).strip().lower()

    if payload.allow_apply is not None:
        opp.allow_apply = bool(payload.allow_apply)

    if payload.allow_external_apply is not None:
        opp.allow_external_apply = bool(payload.allow_external_apply)

    # Track if external URL changed for re-moderation
    old_external_url = opp.external_apply_url
    external_url_changed = False
    
    if "external_apply_url" in payload.model_fields_set:
        url = (payload.external_apply_url or "").strip()
        new_url = url if url else None
        if new_url != old_external_url:
            external_url_changed = True
        opp.external_apply_url = new_url
        
        # If external URL changed, reset approval status to pending
        if external_url_changed and new_url:
            opp.external_url_approved = None  # Pending moderator review
            opp.allow_external_apply = True
        elif external_url_changed and not new_url:
            # URL was removed
            opp.external_url_approved = None
            opp.allow_external_apply = False

    # -------------------------
    # Recompute content_hash (no duplicate blocking on update)
    # -------------------------
    opp.content_hash = opportunity_hash(
        user_id=current_user.id,
        title=opp.title,
        org=opp.org,
        description=opp.description,
        location=opp.location,
        tags=csv_to_tags(opp.tags_csv),
    )

    # -------------------------
    # Re-run AI moderation on FINAL content
    # -------------------------
    class _TempPayload:
        type = opp.type
        title = opp.title
        org = opp.org
        description = opp.description
        location = opp.location
        deadline_text = opp.deadline_text
        contact_email = opp.contact_email
        external_apply_url = opp.external_apply_url
        tags = csv_to_tags(opp.tags_csv)

    mod = await moderate_opportunity_payload(_TempPayload)
    is_flagged = bool(mod.get("flagged"))

    categories = mod.get("categories") or {}
    true_cats = [k for k, v in categories.items() if v]

    # Always flag if AI detects problematic content (hate speech, etc.)
    # This will flag even if the post was previously approved
    if is_flagged:
        opp.is_flagged = True
        opp.flagged_at = datetime.now(timezone.utc)
        opp.flagged_reason = "Auto-flagged by AI moderation"
        opp.flagged_categories = json.dumps(true_cats) if true_cats else None
        
        # If post was previously appealed and approved, clear appeal status for new appeal
        if opp.appeal_status == "approved":
            opp.appeal_status = None
            opp.appeal_message = None
            opp.appeal_at = None
            opp.appeal_response = None
            opp.appeal_decided_at = None
            opp.appeal_decided_by_user_id = None
    else:
        # clean content → auto-unflag ONLY if it was flagged by AI moderation
        # Don't unflag if it was manually flagged by a moderator (e.g., external URL rejection)
        was_ai_flagged = (
            opp.flagged_reason == "Auto-flagged by AI moderation" or
            (opp.flagged_reason and "AI moderation" in opp.flagged_reason)
        )
        if was_ai_flagged:
            opp.is_flagged = False
            opp.flagged_at = None
            opp.flagged_reason = None
            opp.flagged_categories = None
        # If manually flagged (e.g., "External apply URL rejected by moderator"), keep the flag

    # Track when post was last edited (for report restrictions)
    opp.updated_at = datetime.now(timezone.utc)

    # Clear old reports when content changes (allows users to re-report edited content)
    await db.execute(delete(Report).where(Report.opportunity_id == opp.id))

    await db.commit()
    await db.refresh(opp)

    saved_ids = set((await db.execute(
        select(SavedOpportunity.opportunity_id)
        .where(SavedOpportunity.user_id == current_user.id)
    )).scalars().all())

    return opp_to_out(opp, opp.id in saved_ids)




@app.post("/opportunities/{opportunity_id}/report", status_code=201)
async def report_opportunity(
    opportunity_id: int,
    payload: ReportCreate,
    db: DbDep,
    current_user: CurrentUser,
):
    opp = (await db.execute(select(Opportunity).where(Opportunity.id == opportunity_id))).scalar_one_or_none()
    if opp is None:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Opportunity not found"})

    if opp.creator_user_id == current_user.id:
        raise HTTPException(status_code=400, detail={"code": "CANNOT_REPORT_SELF", "message": "You can't report your own post"})

    # Check if post was approved via appeal and hasn't been edited since
    # If so, don't allow new reports (the moderator already reviewed it)
    if opp.appeal_status == "approved" and opp.appeal_decided_at:
        # Allow reports only if the post was edited AFTER the appeal was approved
        if opp.updated_at is None or opp.updated_at <= opp.appeal_decided_at:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "POST_ALREADY_REVIEWED",
                    "message": "This post was already reviewed and approved by a moderator. Reports are only allowed if the creator edits the post."
                }
            )

    r = Report(
        reporter_user_id=current_user.id,
        opportunity_id=opportunity_id,
        reason=payload.reason,
        comment=(payload.comment or "").strip() or None,
    )
    db.add(r)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail={"code": "ALREADY_REPORTED", "message": "You already reported this opportunity"})

    return {"ok": True}



@app.get("/moderation/flagged", response_model=list[MyOpportunityOut])
async def moderation_list_flagged(db: DbDep, current_user: CurrentUser):
    require_moderator(current_user)

    opps = (await db.execute(
        select(Opportunity)
        .where(Opportunity.is_flagged == True)
        .order_by(Opportunity.flagged_at.desc().nullslast(), Opportunity.created_at.desc())
    )).scalars().all()

    # Moderator view: show moderation fields using MyOpportunityOut
    out: list[MyOpportunityOut] = []
    for o in opps:
        base = opp_to_out(o, saved=False).model_dump()
        out.append(MyOpportunityOut(
            **base,
            applications_count=0,
            # you'll add these fields to MyOpportunityOut in schemas.py (next section)
            is_flagged=o.is_flagged,
            flagged_reason=o.flagged_reason,
            flagged_at=o.flagged_at,
            flagged_categories=(json.loads(o.flagged_categories) if o.flagged_categories else []),
        ))
    return out


@app.post("/moderation/opportunities/{opportunity_id}/approve", status_code=200)
async def moderation_approve(opportunity_id: int, db: DbDep, current_user: CurrentUser):
    require_moderator(current_user)

    opp = (await db.execute(select(Opportunity).where(Opportunity.id == opportunity_id))).scalar_one_or_none()
    if opp is None:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Opportunity not found"})

    # Approve = unflag and clear metadata
    opp.is_flagged = False
    opp.flagged_reason = None
    opp.flagged_at = None
    opp.flagged_categories = None

    # Also mark appeal as approved if there was one
    if opp.appeal_status == "pending":
        opp.appeal_status = "approved"
        opp.appeal_decided_at = datetime.now(timezone.utc)
        opp.appeal_decided_by_user_id = current_user.id

    await db.commit()
    return {"ok": True}


# =========================
# Appeals System
# =========================

@app.post("/opportunities/{opportunity_id}/appeal", status_code=201)
async def submit_appeal(
    opportunity_id: int,
    payload: AppealCreate,
    db: DbDep,
    current_user: CurrentUser,
):
    """Creator submits an appeal for their flagged post."""
    opp = (await db.execute(
        select(Opportunity).where(Opportunity.id == opportunity_id)
    )).scalar_one_or_none()

    if opp is None:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Opportunity not found"})

    # Must be the creator
    if opp.creator_user_id != current_user.id:
        raise HTTPException(status_code=403, detail={"code": "FORBIDDEN", "message": "You are not the creator"})

    # Must be flagged
    if not opp.is_flagged:
        raise HTTPException(status_code=400, detail={"code": "NOT_FLAGGED", "message": "This post is not flagged"})

    # Can't appeal if already has pending/decided appeal
    if opp.appeal_status is not None:
        raise HTTPException(status_code=400, detail={"code": "ALREADY_APPEALED", "message": "You have already submitted an appeal"})

    # Submit appeal
    opp.appeal_message = payload.message.strip()
    opp.appeal_at = datetime.now(timezone.utc)
    opp.appeal_status = "pending"

    await db.commit()
    return {"ok": True, "message": "Appeal submitted successfully"}


@app.get("/moderation/appeals", response_model=list[AppealItem])
async def list_appeals(db: DbDep, current_user: CurrentUser):
    """Moderator views pending appeals."""
    require_moderator(current_user)

    # Get flagged opportunities with pending appeals
    stmt = (
        select(Opportunity, User)
        .join(User, User.id == Opportunity.creator_user_id)
        .where(
            Opportunity.is_flagged == True,
            Opportunity.appeal_status == "pending",
        )
        .order_by(Opportunity.appeal_at.desc())
    )
    rows = (await db.execute(stmt)).all()

    out = []
    for opp, creator in rows:
        out.append(AppealItem(
            id=opp.id,
            type=opp.type,
            title=opp.title,
            org=opp.org,
            description=opp.description,
            location=opp.location,
            contact_email=opp.contact_email,
            tags=csv_to_tags(opp.tags_csv),
            is_flagged=opp.is_flagged,
            flagged_reason=opp.flagged_reason,
            flagged_at=opp.flagged_at,
            flagged_categories=(json.loads(opp.flagged_categories) if opp.flagged_categories else []),
            appeal_message=opp.appeal_message,
            appeal_at=opp.appeal_at,
            appeal_status=opp.appeal_status,
            creator_id=creator.id,
            creator_username=creator.username,
        ))
    return out


@app.post("/moderation/appeals/{opportunity_id}/decide", status_code=200)
async def decide_appeal(
    opportunity_id: int,
    payload: AppealDecision,
    db: DbDep,
    current_user: CurrentUser,
):
    """Moderator approves or denies an appeal."""
    require_moderator(current_user)

    opp = (await db.execute(
        select(Opportunity).where(Opportunity.id == opportunity_id)
    )).scalar_one_or_none()

    if opp is None:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Opportunity not found"})

    if opp.appeal_status != "pending":
        raise HTTPException(status_code=400, detail={"code": "NO_PENDING_APPEAL", "message": "No pending appeal for this post"})

    # Update appeal status
    opp.appeal_status = payload.status
    opp.appeal_response = (payload.response or "").strip() or None
    opp.appeal_decided_at = datetime.now(timezone.utc)
    opp.appeal_decided_by_user_id = current_user.id

    # If approved, unflag the post
    if payload.status == "approved":
        opp.is_flagged = False
        opp.flagged_reason = None
        opp.flagged_at = None
        opp.flagged_categories = None
        
        # If the post was rejected due to external URL, reset the external URL status
        # so the post can appear in the dashboard (URL was already cleared on rejection)
        if opp.external_url_approved == False:
            opp.external_url_approved = None
            opp.allow_external_apply = False

    await db.commit()
    return {"ok": True}


# =========================
# Reports Moderation
# =========================

@app.get("/moderation/reports", response_model=list[ReportedOpportunityItem])
async def list_reported_opportunities(db: DbDep, current_user: CurrentUser):
    """Moderator views reported opportunities with all report details."""
    require_moderator(current_user)

    # Get opportunities that have been reported, with report counts
    stmt = (
        select(Opportunity, User, func.count(Report.id).label("reports_count"))
        .join(Report, Report.opportunity_id == Opportunity.id)
        .join(User, User.id == Opportunity.creator_user_id)
        .group_by(Opportunity.id, User.id)
        .order_by(func.count(Report.id).desc())
    )
    rows = (await db.execute(stmt)).all()

    out = []
    for opp, creator, reports_count in rows:
        # Fetch all reports for this opportunity
        reports_stmt = (
            select(Report, User)
            .join(User, User.id == Report.reporter_user_id)
            .where(Report.opportunity_id == opp.id)
            .order_by(Report.created_at.desc())
        )
        report_rows = (await db.execute(reports_stmt)).all()

        reports = [
            ReportItem(
                id=r.id,
                reporter_id=reporter.id,
                reporter_username=reporter.username,
                reason=r.reason,
                comment=r.comment,
                created_at=r.created_at,
            )
            for r, reporter in report_rows
        ]

        out.append(ReportedOpportunityItem(
            id=opp.id,
            type=opp.type,
            title=opp.title,
            org=opp.org,
            description=opp.description,
            location=opp.location,
            contact_email=opp.contact_email,
            tags=csv_to_tags(opp.tags_csv),
            created_at=opp.created_at,
            creator_id=creator.id,
            creator_username=creator.username,
            reports_count=reports_count,
            reports=reports,
        ))

    return out


@app.post("/moderation/reports/{opportunity_id}/decide", status_code=200)
async def decide_reports(
    opportunity_id: int,
    payload: ReportDecision,
    db: DbDep,
    current_user: CurrentUser,
):
    """Moderator dismisses reports or takes down the post."""
    require_moderator(current_user)

    opp = (await db.execute(
        select(Opportunity).where(Opportunity.id == opportunity_id)
    )).scalar_one_or_none()

    if opp is None:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Opportunity not found"})

    # Check there are reports for this opportunity
    report_count = (await db.execute(
        select(func.count(Report.id)).where(Report.opportunity_id == opportunity_id)
    )).scalar_one()

    if report_count == 0:
        raise HTTPException(status_code=400, detail={"code": "NO_REPORTS", "message": "No reports for this post"})

    if payload.action == "dismiss":
        # Clear all reports - they've been reviewed and dismissed
        await db.execute(delete(Report).where(Report.opportunity_id == opportunity_id))
        await db.commit()
        return {"ok": True, "message": "Reports dismissed"}

    elif payload.action == "take_down":
        # Flag the post and record reason
        opp.is_flagged = True
        opp.flagged_at = datetime.now(timezone.utc)
        opp.flagged_reason = f"Taken down by moderator: {(payload.reason or 'User reports').strip()}"
        
        # Clear previous appeal status so user can appeal again (new flagging event)
        opp.appeal_status = None
        opp.appeal_message = None
        opp.appeal_at = None
        opp.appeal_response = None
        opp.appeal_decided_at = None
        opp.appeal_decided_by_user_id = None

        # Clear the reports since action was taken
        await db.execute(delete(Report).where(Report.opportunity_id == opportunity_id))
        await db.commit()
        return {"ok": True, "message": "Post taken down"}

    return {"ok": False}


# =========================
# External URL Moderation
# =========================
@app.get("/moderation/external-urls", response_model=list[ExternalUrlItem])
async def list_pending_external_urls(db: DbDep, current_user: CurrentUser):
    """Moderator views opportunities with external URLs pending approval."""
    require_moderator(current_user)

    stmt = (
        select(Opportunity, User)
        .join(User, User.id == Opportunity.creator_user_id)
        .where(
            Opportunity.allow_external_apply == True,
            Opportunity.external_apply_url.isnot(None),
            Opportunity.external_url_approved.is_(None),  # Pending approval
        )
        .order_by(Opportunity.created_at.desc())
    )
    rows = (await db.execute(stmt)).all()

    out = []
    for opp, creator in rows:
        out.append(ExternalUrlItem(
            id=opp.id,
            type=opp.type,
            title=opp.title,
            org=opp.org,
            description=opp.description,
            location=opp.location,
            contact_email=opp.contact_email,
            tags=csv_to_tags(opp.tags_csv),
            external_apply_url=opp.external_apply_url,
            created_at=opp.created_at,
            creator_id=creator.id,
            creator_username=creator.username,
        ))
    return out


@app.post("/moderation/external-urls/{opportunity_id}/decide", status_code=200)
async def decide_external_url(
    opportunity_id: int,
    payload: ExternalUrlDecision,
    db: DbDep,
    current_user: CurrentUser,
):
    """Moderator approves or rejects an external URL."""
    require_moderator(current_user)

    # 1) load opportunity
    opp = (await db.execute(
        select(Opportunity).where(Opportunity.id == opportunity_id)
    )).scalar_one_or_none()

    if opp is None:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Opportunity not found"})

    if not opp.external_apply_url:
        raise HTTPException(status_code=400, detail={"code": "NO_EXTERNAL_URL", "message": "This opportunity has no external URL"})

    # 2) decide
    opp.external_url_approved = payload.approved

    if payload.approved:
        # approved -> keep post public, no takedown
        # (optional: if it was previously flagged only for this, you could unflag here)
        pass
    else:
        # rejected -> take down from public feed
        opp.is_flagged = True
        opp.flagged_at = datetime.now(timezone.utc)
        opp.flagged_reason = "External apply URL rejected by moderator"
        
        # Clear previous appeal status so user can appeal again (new flagging event)
        opp.appeal_status = None
        opp.appeal_message = None
        opp.appeal_at = None
        opp.appeal_response = None
        opp.appeal_decided_at = None
        opp.appeal_decided_by_user_id = None

        # remove external apply fields
        opp.allow_external_apply = False
        opp.external_apply_url = None

    await db.commit()
    return {"ok": True, "approved": payload.approved}


def _get_link_info_for_opportunity(opp: Opportunity) -> tuple[str, str, bool, bool, str, list]:
    """Validate, normalize, and compute risk. Returns (normalized_url, host, is_https, allowlisted, risk_level, reasons). Raises HTTPException on invalid URL."""
    raw = (opp.external_apply_url or "").strip()
    if not raw:
        raise HTTPException(status_code=400, detail={"code": "NO_EXTERNAL_URL", "message": "This opportunity has no external URL"})
    normalized, err = url_safety.validate_and_normalize_url(raw)
    if err:
        raise HTTPException(status_code=400, detail={"code": "INVALID_URL", "message": err})
    risk_level, allowlisted, reasons = url_safety.compute_risk(normalized)
    parsed = urlparse(normalized)
    host = (parsed.netloc or "").split(":")[0].lower()
    is_https = (parsed.scheme or "").lower() == "https"
    return normalized, host, is_https, allowlisted, risk_level, reasons


@app.get("/moderation/external-urls/{opportunity_id}/link-info", response_model=LinkInfoOut)
async def get_external_url_link_info(
    opportunity_id: int,
    db: DbDep,
    current_user: CurrentUser,
):
    """Return validated/normalized URL and risk info for display in modal. No logging."""
    require_moderator(current_user)
    opp = (await db.execute(
        select(Opportunity).where(Opportunity.id == opportunity_id)
    )).scalar_one_or_none()
    if opp is None:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Opportunity not found"})
    normalized, host, is_https, allowlisted, risk_level, reasons = _get_link_info_for_opportunity(opp)
    return LinkInfoOut(
        normalized_url=normalized,
        host=host,
        is_https=is_https,
        allowlisted=allowlisted,
        risk_level=risk_level,
        reasons=reasons,
    )


@app.post("/moderation/external-urls/{opportunity_id}/open-in-sandbox", response_model=OpenInSandboxOut, status_code=200)
async def open_external_url_in_sandbox(
    opportunity_id: int,
    payload: OpenInSandboxAction,
    request: Request,
    db: DbDep,
    current_user: CurrentUser,
):
    """
    Safe External Link Review: validate/normalize URL, log action (open or copy), return safe payload.
    Only http/https allowed; dangerous schemes refused. Frontend opens normalized_url in new tab or copies to clipboard.
    """
    require_moderator(current_user)
    opp = (await db.execute(
        select(Opportunity).where(Opportunity.id == opportunity_id)
    )).scalar_one_or_none()
    if opp is None:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Opportunity not found"})
    normalized, host, is_https, allowlisted, risk_level, reasons = _get_link_info_for_opportunity(opp)
    action = payload.action.upper()  # OPEN or COPY
    user_agent = (request.headers.get("user-agent") or "")[:500]
    client_host = request.client.host if request.client else None
    if client_host and len(client_host) > 45:
        client_host = client_host[:45]
    log_entry = ModerationLinkOpen(
        opportunity_id=opp.id,
        moderator_user_id=current_user.id,
        action=action,
        normalized_url=normalized,
        host=host,
        risk_level=risk_level,
        reasons=json.dumps(reasons) if reasons else None,
        user_agent=user_agent or None,
        ip=client_host,
    )
    db.add(log_entry)
    await db.commit()
    return OpenInSandboxOut(
        normalized_url=normalized,
        host=host,
        is_https=is_https,
        allowlisted=allowlisted,
        risk_level=risk_level,
        reasons=reasons,
    )


# =========================
# Contact / Email
# =========================

@app.post("/contact", status_code=200)
async def send_contact_email(
    payload: ContactCreate,
    current_user: CurrentUser,
):
    """Send a contact/feedback email using Resend."""
    resend_api_key = os.environ.get("RESEND_API_KEY")
    contact_email = os.environ.get("CONTACT_EMAIL", "contact@opportunityhub.com")
    
    if not resend_api_key:
        raise HTTPException(
            status_code=500,
            detail={"code": "EMAIL_NOT_CONFIGURED", "message": "Email service is not configured"}
        )
    
    try:
        import httpx
        
        # Use Resend's test domain if no custom domain is configured
        # For production, you'll need to verify your own domain in Resend
        resend_domain = os.environ.get("RESEND_DOMAIN")
        if resend_domain:
            from_email = f"Opportunity Hub <noreply@{resend_domain}>"
        else:
            # Use Resend's test domain (works without domain verification)
            from_email = "Opportunity Hub <onboarding@resend.dev>"
        
        # Send email via Resend API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {resend_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "from": from_email,
                    "to": [contact_email],
                    "subject": f"Contact Form: Message from {current_user.username}",
                    "html": f"""
                    <h2>New Contact Form Submission</h2>
                    <p><strong>From:</strong> {current_user.username} ({current_user.email})</p>
                    <p><strong>User ID:</strong> {current_user.id}</p>
                    <p><strong>Message:</strong></p>
                    <p style="white-space: pre-wrap;">{payload.message}</p>
                    """,
                    "text": f"""
New Contact Form Submission

From: {current_user.username} ({current_user.email})
User ID: {current_user.id}

Message:
{payload.message}
                    """.strip(),
                },
                timeout=10.0,
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail={"code": "EMAIL_SEND_FAILED", "message": "Failed to send email"}
                )
        
        return {"ok": True, "message": "Your message has been sent successfully"}
        
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail={"code": "EMAIL_LIBRARY_MISSING", "message": "Email library not installed. Install httpx: pip install httpx"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": "EMAIL_ERROR", "message": f"Error sending email: {str(e)}"}
        )
