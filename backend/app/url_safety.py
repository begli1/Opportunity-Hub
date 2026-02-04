"""
URL validation, normalization, and risk scoring for moderator external-link review.
Only http/https allowed; dangerous schemes blocked; optional allowlist and risk signals.
"""
from urllib.parse import urlparse, urlunparse
import re
from typing import Tuple, List

MAX_URL_LENGTH = 2048
BLOCKED_SCHEMES = frozenset({
    "javascript", "data", "file", "chrome", "about", "blob", "vbscript",
    "vnd", "ms-help", "ms-its", "mhtml", "res", "x-rss", "feed",
})
ALLOWED_SCHEMES = frozenset({"http", "https"})

# Common job/application domains (lowercase, no port). Extend as needed.
# Common student / internship / volunteering / tutoring platforms
# Lowercase, no ports. Use suffix matching in code (endswith check).

ALLOWLIST_DOMAINS = frozenset({

    # ===== Professional / Job / Internship Platforms =====
    "linkedin.com", "www.linkedin.com",
    "indeed.com", "www.indeed.com",
    "glassdoor.com", "www.glassdoor.com",
    "ziprecruiter.com", "www.ziprecruiter.com",
    "monster.com", "www.monster.com",
    "careerbuilder.com", "www.careerbuilder.com",

    "handshake.com", "www.handshake.com",
    "app.joinhandshake.com", "joinhandshake.com",

    "apply.workable.com", "workable.com",
    "jobs.lever.co", "lever.co",
    "greenhouse.io", "boards.greenhouse.io",
    "smartrecruiters.com", "www.smartrecruiters.com",

    "myworkdayjobs.com", "workday.com",
    "icims.com", "careers.icims.com",

    # ===== Government / Public Programs =====
    "usajobs.gov", "www.usajobs.gov",
    "intern.usajobs.gov",
    "nsf.gov", "www.nsf.gov",
    "nih.gov", "www.nih.gov",
    "nasa.gov", "www.nasa.gov",
    "usa.gov", "www.usa.gov",

    # ===== Research / Academic / Summer Programs =====
    "nsf.org",
    "pathwaystoscience.org",
    "research.gov",
    "sciencepathways.org",

    "summerapply.com",
    "apply.commonapp.org",
    "commonapp.org",

    "collegeboard.org", "www.collegeboard.org",
    "ets.org", "www.ets.org",

    # ===== Volunteering / Nonprofit Platforms =====
    "volunteermatch.org", "www.volunteermatch.org",
    "idealist.org", "www.idealist.org",
    "catchafire.org", "www.catchafire.org",
    "justserve.org", "www.justserve.org",
    "points-of-light.org", "www.pointsoflight.org",

    "redcross.org", "www.redcross.org",
    "habitat.org", "www.habitat.org",
    "ymca.org", "www.ymca.org",
    "unitedway.org", "www.unitedway.org",

    # ===== Tutoring / Education / Mentoring =====
    "chegg.com", "www.chegg.com",
    "wyzant.com", "www.wyzant.com",
    "care.com", "www.care.com",

    "tutor.com", "www.tutor.com",
    "skooli.com", "www.skooli.com",
    "varsitytutors.com", "www.varsitytutors.com",

    "khanacademy.org", "www.khanacademy.org",
    "coursera.org", "www.coursera.org",
    "edx.org", "www.edx.org",
    "udemy.com", "www.udemy.com",

    # ===== Forms / Applications / Data Collection =====
    "google.com", "www.google.com",
    "docs.google.com", "forms.google.com",

    "typeform.com", "form.typeform.com",
    "jotform.com", "www.jotform.com",

    "airtable.com", "www.airtable.com",
    "notion.so", "www.notion.so",

    # ===== Fellowship / Youth / Leadership Programs =====
    "scholarships.com", "www.scholarships.com",
    "fastweb.com", "www.fastweb.com",
    "cheggscholarships.com",

    "civicsunplugged.org",
    "rise.org",
    "questbridge.org", "www.questbridge.org",

    "jackierobinson.org",
    "thurgoodmarshallfund.org",

    # ===== Tech / Startup Internships =====
    "ycombinator.com", "www.ycombinator.com",
    "angel.co", "wellfound.com",
    "internshala.com",

    # ===== Nonprofit / International Orgs =====
    "un.org", "www.un.org",
    "unicef.org", "www.unicef.org",
    "who.int", "www.who.int",

    "peacecorps.gov", "www.peacecorps.gov",

})



def _normalize_host(host: str) -> str:
    """Strip port and lowercase."""
    if not host:
        return ""
    return host.split(":")[0].lower().strip()


def _is_ip_literal(host: str) -> bool:
    """True if host is IP v4 or v6 literal."""
    if not host:
        return False
    # IPv4
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", host):
        return True
    # IPv6 bracket form
    if host.startswith("[") and "]" in host:
        return True
    return False


def validate_and_normalize_url(raw: str) -> Tuple[str | None, str]:
    """
    Validate and normalize URL. Returns (normalized_url, error_message).
    If error_message is non-empty, normalized_url is None.
    - Only http/https allowed; block dangerous schemes.
    - Default to https:// if no scheme.
    - Max length 2048.
    """
    if not raw or not isinstance(raw, str):
        return None, "URL is empty"
    s = raw.strip()
    if len(s) > MAX_URL_LENGTH:
        return None, f"URL exceeds maximum length ({MAX_URL_LENGTH})"

    # Scheme check before parsing (avoid parsing javascript: etc.)
    if ":" in s:
        scheme = s.split(":", 1)[0].lower().strip()
        if scheme in BLOCKED_SCHEMES:
            return None, f"Dangerous scheme not allowed: {scheme}"
        if scheme not in ALLOWED_SCHEMES:
            return None, f"Only http and https are allowed; got: {scheme}"
    else:
        s = "https://" + s

    try:
        parsed = urlparse(s)
    except Exception as e:
        return None, f"Invalid URL: {e}"

    scheme = (parsed.scheme or "https").lower()
    if scheme not in ALLOWED_SCHEMES:
        return None, f"Only http and https are allowed; got: {scheme}"

    netloc = (parsed.netloc or "").strip()
    if not netloc:
        return None, "URL has no host"

    # Rebuild normalized URL (https preferred for safety)
    normalized = urlunparse((
        "https" if scheme == "https" else "http",
        netloc,
        parsed.path or "/",
        parsed.params,
        parsed.query,
        parsed.fragment or "",
    ))
    if len(normalized) > MAX_URL_LENGTH:
        return None, f"URL exceeds maximum length ({MAX_URL_LENGTH})"
    return normalized, ""


def compute_risk(normalized_url: str) -> Tuple[str, bool, List[str]]:
    """
    Returns (risk_level, allowlisted, reasons).
    risk_level: "LOW" | "MEDIUM" | "HIGH"
    """
    reasons: List[str] = []
    try:
        parsed = urlparse(normalized_url)
    except Exception:
        return "HIGH", False, ["Failed to parse URL"]

    host = _normalize_host(parsed.netloc or "")
    is_https = (parsed.scheme or "").lower() == "https"
    allowlisted = host in ALLOWLIST_DOMAINS or any(
        host == d or host.endswith("." + d) for d in ALLOWLIST_DOMAINS
    )

    if not is_https:
        reasons.append("non-HTTPS")
    if _is_ip_literal(host):
        reasons.append("IP literal host")
    if len(normalized_url) > 500:
        reasons.append("very long URL")
    if not allowlisted:
        reasons.append("domain not allowlisted")

    if _is_ip_literal(host) or (not is_https and not allowlisted):
        risk_level = "HIGH"
    elif not allowlisted or not is_https or len(normalized_url) > 500:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return risk_level, allowlisted, reasons
