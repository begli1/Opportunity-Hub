# schemas.py
from datetime import datetime
from typing import List, Optional, Literal

from pydantic import BaseModel, EmailStr, Field


# =========================
# Applications inbox
# =========================
class ApplicationInboxItem(BaseModel):
    opportunity_id: int
    title: str
    org: str
    type: str
    applications_count: int
    latest_application_at: Optional[datetime] = None


class ApplicationInboxOut(BaseModel):
    items: List[ApplicationInboxItem]



class ReportCreate(BaseModel):
    reason: Literal["scam", "inappropriate", "fake_org", "spam", "other"]
    comment: Optional[str] = ""


# =========================
# Users / Auth
# =========================
class UserBase(BaseModel):
    username: str = Field(..., max_length=25, description="Unique username")
    email: EmailStr = Field(..., description="User email")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Plain password input for signup")


class LoginByEmail(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: int
    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int  # seconds until expiry


class OpportunityOut(BaseModel):
    id: int
    type: str
    title: str
    org: str
    description: str
    location: str

    deadline_at: Optional[datetime] = None
    deadline_text: str = ""

    tags: List[str] = Field(default_factory=list)
    saved: bool

    contact_email: str
    allow_apply: bool
    allow_external_apply: bool
    external_apply_url: Optional[str] = None
    external_url_approved: Optional[bool] = None  # None=pending, True=approved, False=rejected

class ApplicationOut(BaseModel):
    id: int
    opportunity_id: int
    applicant_user_id: int
    full_name: str
    email: EmailStr
    message: str
    created_at: datetime

    status: str
    decision_reason: Optional[str] = None
    decided_at: Optional[datetime] = None
    decided_by_user_id: Optional[int] = None


# =========================
# Dashboard
# =========================
class DashboardStats(BaseModel):
    newMatches: int
    saved: int
    applications: int


class DashboardOut(BaseModel):
    me: UserOut
    stats: DashboardStats
    trending: List[OpportunityOut]
    saved: List[OpportunityOut]





# ---------- Opportunities ----------



class OpportunityCreate(BaseModel):
    type: str
    title: str
    org: str
    description: str
    location: str

    deadline_at: Optional[datetime] = None
    deadline_text: str = ""

    tags: List[str] = Field(default_factory=list)

    contact_email: EmailStr
    allow_apply: bool = True
    allow_external_apply: bool = False
    external_apply_url: Optional[str] = None

    # Honeypot field - should always be empty from real users
    website: Optional[str] = None


# ✅ NEW: update schema for editing posts (all optional)
class OpportunityUpdate(BaseModel):
    type: Optional[str] = None
    title: Optional[str] = None
    org: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None

    deadline_at: Optional[datetime] = None
    deadline_text: Optional[str] = None

    tags: Optional[List[str]] = None

    contact_email: Optional[EmailStr] = None
    allow_apply: Optional[bool] = None
    allow_external_apply: Optional[bool] = None
    external_apply_url: Optional[str] = None


# ✅ NEW: for "My posts" list with application counts
class MyOpportunityOut(OpportunityOut):
    applications_count: int = 0

    # moderation fields (creator + moderator views)
    is_flagged: bool = False
    flagged_reason: Optional[str] = None
    flagged_at: Optional[datetime] = None
    flagged_categories: List[str] = Field(default_factory=list)

    # appeal fields (creator can see their appeal status)
    appeal_message: Optional[str] = None
    appeal_at: Optional[datetime] = None
    appeal_status: Optional[str] = None  # pending/approved/denied
    appeal_response: Optional[str] = None
    appeal_decided_at: Optional[datetime] = None



class MyApplicationItem(BaseModel):
    application: ApplicationOut
    opportunity: OpportunityOut

# ---------- Applications ----------
class ApplicationCreate(BaseModel):
    full_name: str
    email: EmailStr
    message: str = ""


# ✅ UPDATED: include status + decision fields


# ✅ NEW: creator decision input
class ApplicationDecisionIn(BaseModel):
    status: Literal["accepted", "rejected"]
    reason: Optional[str] = ""


# =========================
# Appeals System
# =========================
class AppealCreate(BaseModel):
    message: str = Field(..., min_length=10, max_length=1000, description="Why should this post be approved?")


class AppealDecision(BaseModel):
    status: Literal["approved", "denied"]
    response: Optional[str] = ""


# For moderator view - opportunity with appeal info
class AppealItem(BaseModel):
    id: int
    type: str
    title: str
    org: str
    description: str
    location: str
    contact_email: str
    tags: List[str] = Field(default_factory=list)

    # Flagged info
    is_flagged: bool
    flagged_reason: Optional[str] = None
    flagged_at: Optional[datetime] = None
    flagged_categories: List[str] = Field(default_factory=list)

    # Appeal info
    appeal_message: Optional[str] = None
    appeal_at: Optional[datetime] = None
    appeal_status: Optional[str] = None

    # Creator info
    creator_id: int
    creator_username: str


# =========================
# Reports Moderation
# =========================
class ReportItem(BaseModel):
    id: int
    reporter_id: int
    reporter_username: str
    reason: str
    comment: Optional[str] = None
    created_at: datetime


class ReportedOpportunityItem(BaseModel):
    id: int
    type: str
    title: str
    org: str
    description: str
    location: str
    contact_email: str
    tags: List[str] = Field(default_factory=list)
    created_at: datetime

    # Creator info
    creator_id: int
    creator_username: str

    # Report aggregates
    reports_count: int
    reports: List[ReportItem] = Field(default_factory=list)


class ReportDecision(BaseModel):
    action: Literal["dismiss", "take_down"]
    reason: Optional[str] = ""


# =========================
# External URL Moderation
# =========================
class ExternalUrlItem(BaseModel):
    id: int
    type: str
    title: str
    org: str
    description: str
    location: str
    contact_email: str
    tags: List[str] = Field(default_factory=list)
    external_apply_url: str
    created_at: datetime

    # Creator info
    creator_id: int
    creator_username: str


class ExternalUrlDecision(BaseModel):
    approved: bool


class LinkInfoOut(BaseModel):
    """Validated/normalized URL and risk info (no logging)."""
    normalized_url: str
    host: str
    is_https: bool
    allowlisted: bool
    risk_level: str  # LOW, MEDIUM, HIGH
    reasons: List[str] = Field(default_factory=list)


class OpenInSandboxAction(BaseModel):
    """Action to log: open or copy."""
    action: Literal["open", "copy"] = "open"


class OpenInSandboxOut(BaseModel):
    """Response after logging open/copy; frontend uses normalized_url to open or copy."""
    ok: bool = True
    normalized_url: str
    host: str
    is_https: bool
    allowlisted: bool
    risk_level: str
    reasons: List[str] = Field(default_factory=list)


# =========================
# Contact / Email
# =========================
class ContactCreate(BaseModel):
    message: str = Field(..., min_length=10, max_length=2000, description="Contact message")
