from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import math
import re
from typing import Iterable, Optional

from .schemas import OpportunityOut


STOP_WORDS = {
    "a", "about", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "into",
    "is", "it", "of", "on", "or", "our", "that", "the", "their", "this", "to", "with", "you",
    "your", "student", "students", "opportunity", "opportunities", "resource", "resources",
    "program", "programs", "community", "help", "helps",
}


@dataclass(frozen=True)
class OpportunityFingerprint:
    id: int
    saved: bool
    featured: bool
    type_key: str
    org_key: str
    tag_phrases: frozenset[str]
    tag_tokens: frozenset[str]
    keyword_tokens: frozenset[str]
    location_tokens: frozenset[str]
    created_at: Optional[datetime]
    popularity: float


@dataclass(frozen=True)
class InterestProfile:
    tag_phrase_weights: Counter[str]
    tag_token_weights: Counter[str]
    keyword_weights: Counter[str]
    org_weights: Counter[str]
    location_weights: Counter[str]
    type_weights: Counter[str]
    saved_fingerprints: tuple[OpportunityFingerprint, ...]


@dataclass(frozen=True)
class RarityMaps:
    phrase_rarity: dict[str, float]
    token_rarity: dict[str, float]


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", (value or "").lower())).strip()


def simplify_plural(token: str) -> str:
    value = (token or "").strip().lower()
    if len(value) <= 3:
        return value
    if value.endswith("ies") and len(value) > 5:
        return f"{value[:-3]}y"
    if value.endswith("ing") and len(value) > 5:
        return value[:-3]
    if value.endswith("ed") and len(value) > 4:
        return value[:-2]
    if value.endswith("s") and not value.endswith("ss") and len(value) > 4:
        return value[:-1]
    return value


def tokenize_text(*parts: Optional[str]) -> list[str]:
    tokens: list[str] = []
    for part in parts:
        normalized = normalize_text(part or "")
        if not normalized:
            continue
        for raw in normalized.split():
            token = simplify_plural(raw)
            if len(token) < 3 or token in STOP_WORDS:
                continue
            tokens.append(token)
    return list(dict.fromkeys(tokens))


def normalize_tags(tags: Iterable[str]) -> list[str]:
    phrases: list[str] = []
    for tag in tags or []:
        normalized = normalize_text(tag)
        if normalized:
            phrases.append(normalized)
    return list(dict.fromkeys(phrases))


def build_fingerprint(
    opportunity: OpportunityOut,
    popularity_by_id: dict[int, int],
    featured_ids: set[int],
) -> OpportunityFingerprint:
    tag_phrases = normalize_tags(opportunity.tags)
    tag_tokens = tokenize_text(*tag_phrases)
    keyword_tokens = tokenize_text(
        opportunity.title,
        opportunity.description,
        opportunity.org,
    )
    location_tokens = tokenize_text(opportunity.location)

    return OpportunityFingerprint(
        id=opportunity.id,
        saved=bool(opportunity.saved),
        featured=opportunity.id in featured_ids,
        type_key=normalize_text(opportunity.type),
        org_key=normalize_text(opportunity.org),
        tag_phrases=frozenset(tag_phrases),
        tag_tokens=frozenset(tag_tokens),
        keyword_tokens=frozenset(keyword_tokens),
        location_tokens=frozenset(location_tokens),
        created_at=opportunity.created_at,
        popularity=float(popularity_by_id.get(opportunity.id, 0)),
    )


def build_interest_profile(saved_posts: list[OpportunityFingerprint]) -> InterestProfile:
    tag_phrase_weights: Counter[str] = Counter()
    tag_token_weights: Counter[str] = Counter()
    keyword_weights: Counter[str] = Counter()
    org_weights: Counter[str] = Counter()
    location_weights: Counter[str] = Counter()
    type_weights: Counter[str] = Counter()

    for post in saved_posts:
        for phrase in post.tag_phrases:
            tag_phrase_weights[phrase] += 3.5
        for token in post.tag_tokens:
            tag_token_weights[token] += 2.0
        for token in post.keyword_tokens:
            keyword_weights[token] += 1.0
        for token in post.location_tokens:
            location_weights[token] += 0.7
        if post.org_key:
            org_weights[post.org_key] += 0.8
        if post.type_key:
            type_weights[post.type_key] += 0.45

    return InterestProfile(
        tag_phrase_weights=tag_phrase_weights,
        tag_token_weights=tag_token_weights,
        keyword_weights=keyword_weights,
        org_weights=org_weights,
        location_weights=location_weights,
        type_weights=type_weights,
        saved_fingerprints=tuple(saved_posts),
    )


def build_rarity_maps(fingerprints: list[OpportunityFingerprint]) -> RarityMaps:
    phrase_counts: Counter[str] = Counter()
    token_counts: Counter[str] = Counter()
    total_docs = max(1, len(fingerprints))

    for fingerprint in fingerprints:
        for phrase in set(fingerprint.tag_phrases):
            phrase_counts[phrase] += 1
        combined_tokens = set(fingerprint.tag_tokens) | set(fingerprint.keyword_tokens) | set(fingerprint.location_tokens)
        for token in combined_tokens:
            token_counts[token] += 1

    phrase_rarity = {
        phrase: 1.0 + math.log((total_docs + 1) / (count + 1))
        for phrase, count in phrase_counts.items()
    }
    token_rarity = {
        token: 1.0 + math.log((total_docs + 1) / (count + 1))
        for token, count in token_counts.items()
    }

    return RarityMaps(phrase_rarity=phrase_rarity, token_rarity=token_rarity)


def score_weighted_overlap(
    values: Iterable[str],
    weights: Counter[str],
    rarity: dict[str, float],
    multiplier: float,
) -> tuple[float, int]:
    score = 0.0
    matches = 0
    for value in values:
        weight = weights.get(value)
        if not weight:
            continue
        score += weight * rarity.get(value, 1.0) * multiplier
        matches += 1
    return score, matches


def count_matching_saved_posts(candidate: OpportunityFingerprint, saved_posts: tuple[OpportunityFingerprint, ...]) -> int:
    matches = 0
    for saved in saved_posts:
        if saved.id == candidate.id:
            continue
        exact_tags = candidate.tag_phrases & saved.tag_phrases
        shared_tag_tokens = candidate.tag_tokens & saved.tag_tokens
        shared_keywords = candidate.keyword_tokens & saved.keyword_tokens
        if exact_tags or shared_tag_tokens or len(shared_keywords) >= 2:
            matches += 1
    return matches


def compute_freshness_boost(created_at: Optional[datetime], now: datetime) -> float:
    if created_at is None:
        return 0.0
    created = created_at if created_at.tzinfo else created_at.replace(tzinfo=timezone.utc)
    age_days = max(0.0, (now - created).total_seconds() / 86400)
    return max(0.0, 2.4 - min(age_days, 21) * 0.11)


def compute_cold_start_score(
    candidate: OpportunityFingerprint,
    now: datetime,
    preferred_location_tokens: frozenset[str],
) -> float:
    score = compute_freshness_boost(candidate.created_at, now)
    score += math.log1p(candidate.popularity) * 1.2
    if candidate.featured:
        score += 2.0
    if preferred_location_tokens and candidate.location_tokens:
        score += len(candidate.location_tokens & preferred_location_tokens) * 0.8
    return score - (1.0 if candidate.saved else 0.0)


def score_candidate(
    candidate: OpportunityFingerprint,
    profile: InterestProfile,
    rarity: RarityMaps,
    now: datetime,
    preferred_location_tokens: frozenset[str],
) -> tuple[float, dict[str, float]]:
    exact_tag_score, exact_tag_matches = score_weighted_overlap(
        candidate.tag_phrases,
        profile.tag_phrase_weights,
        rarity.phrase_rarity,
        2.8,
    )
    tag_token_score, tag_token_matches = score_weighted_overlap(
        candidate.tag_tokens,
        profile.tag_token_weights,
        rarity.token_rarity,
        1.8,
    )
    keyword_score, keyword_matches = score_weighted_overlap(
        candidate.keyword_tokens,
        profile.keyword_weights,
        rarity.token_rarity,
        0.9,
    )
    location_score, location_matches = score_weighted_overlap(
        candidate.location_tokens,
        profile.location_weights,
        rarity.token_rarity,
        0.6,
    )

    type_score = profile.type_weights.get(candidate.type_key, 0.0) * 0.8
    org_score = profile.org_weights.get(candidate.org_key, 0.0) * 1.1
    popularity_score = math.log1p(candidate.popularity) * 0.25
    freshness_score = compute_freshness_boost(candidate.created_at, now)
    featured_score = 1.2 if candidate.featured else 0.0
    saved_penalty = 1.35 if candidate.saved else 0.0

    matched_saved_posts = count_matching_saved_posts(candidate, profile.saved_fingerprints)
    multi_match_bonus = max(0, matched_saved_posts - 1) * 1.85

    if preferred_location_tokens and candidate.location_tokens:
        location_score += len(candidate.location_tokens & preferred_location_tokens) * 0.35

    breakdown = {
        "exact_tag": exact_tag_score,
        "tag_token": tag_token_score,
        "keyword": keyword_score,
        "location": location_score,
        "org": org_score,
        "type": type_score,
        "popularity": popularity_score,
        "freshness": freshness_score,
        "featured": featured_score,
        "multi_match": multi_match_bonus,
        "saved_penalty": -saved_penalty,
        "strong_matches": float(exact_tag_matches + tag_token_matches),
        "keyword_matches": float(keyword_matches + location_matches),
        "matched_saved_posts": float(matched_saved_posts),
    }

    total = (
        exact_tag_score
        + tag_token_score
        + keyword_score
        + location_score
        + org_score
        + type_score
        + popularity_score
        + freshness_score
        + featured_score
        + multi_match_bonus
        - saved_penalty
    )
    return total, breakdown


def diversify_ranked_results(
    scored_items: list[tuple[OpportunityOut, OpportunityFingerprint, float, dict[str, float]]],
) -> list[OpportunityOut]:
    remaining = list(scored_items)
    diversified: list[OpportunityOut] = []
    org_counts: Counter[str] = Counter()
    tag_counts: Counter[str] = Counter()

    while remaining:
        best_index = 0
        best_adjusted_score = None

        for index, (_, fingerprint, base_score, _) in enumerate(remaining):
            org_penalty = org_counts[fingerprint.org_key] * 1.6 if fingerprint.org_key else 0.0
            tag_penalty = sum(tag_counts[tag] for tag in fingerprint.tag_phrases) * 0.22
            adjusted_score = base_score - org_penalty - tag_penalty
            if best_adjusted_score is None or adjusted_score > best_adjusted_score:
                best_adjusted_score = adjusted_score
                best_index = index

        opportunity, fingerprint, _, _ = remaining.pop(best_index)
        diversified.append(opportunity)
        if fingerprint.org_key:
            org_counts[fingerprint.org_key] += 1
        for tag in fingerprint.tag_phrases:
            tag_counts[tag] += 1

    return diversified


def recommend_for_user(
    opportunities: list[OpportunityOut],
    saved_posts: list[OpportunityOut],
    popularity_by_id: Optional[dict[int, int]] = None,
    featured_ids: Optional[set[int]] = None,
    preferred_location: Optional[str] = None,
    limit: Optional[int] = None,
) -> list[OpportunityOut]:
    if not opportunities:
        return []

    popularity_by_id = popularity_by_id or {}
    featured_ids = featured_ids or set()
    preferred_location_tokens = frozenset(tokenize_text(preferred_location or ""))
    now = datetime.now(timezone.utc)

    candidate_fingerprints = {
        opportunity.id: build_fingerprint(opportunity, popularity_by_id, featured_ids)
        for opportunity in opportunities
    }

    if not saved_posts:
        cold_ranked = sorted(
            opportunities,
            key=lambda opportunity: compute_cold_start_score(
                candidate_fingerprints[opportunity.id],
                now,
                preferred_location_tokens,
            ),
            reverse=True,
        )
        return cold_ranked[:limit] if limit else cold_ranked

    saved_fingerprints = [
        build_fingerprint(opportunity, popularity_by_id, featured_ids)
        for opportunity in saved_posts
    ]
    profile = build_interest_profile(saved_fingerprints)
    rarity = build_rarity_maps(list(candidate_fingerprints.values()) + saved_fingerprints)

    scored_items: list[tuple[OpportunityOut, OpportunityFingerprint, float, dict[str, float]]] = []
    for opportunity in opportunities:
        fingerprint = candidate_fingerprints[opportunity.id]
        score, breakdown = score_candidate(
            fingerprint,
            profile,
            rarity,
            now,
            preferred_location_tokens,
        )
        strong_matches = breakdown["strong_matches"]
        keyword_matches = breakdown["keyword_matches"]
        if score < 5.0:
            continue
        if strong_matches < 1 and keyword_matches < 2:
            continue
        scored_items.append((opportunity, fingerprint, score, breakdown))

    scored_items.sort(key=lambda item: item[2], reverse=True)
    diversified = diversify_ranked_results(scored_items)
    return diversified[:limit] if limit else diversified
