"""Simple Phase 1 similar incident scoring."""

import re

from app.schemas.similar_incident_schema import (
    SimilarIncidentMatch,
    SimilarIncidentRequest,
    SimilarIncidentResponse,
)

WORD_PATTERN = re.compile(r"[a-z0-9]+")


def _keywords(value: str) -> set[str]:
    return {
        word
        for word in WORD_PATTERN.findall(value.lower())
        if len(word) > 2
    }


def score_similar_incidents(
    payload: SimilarIncidentRequest,
) -> SimilarIncidentResponse:
    current_root_words = _keywords(payload.root_cause)
    current_alert_types = {value.value for value in payload.alert_types}
    matches: list[SimilarIncidentMatch] = []

    for historical in payload.historical_incidents:
        score = 0
        if historical.service_name == payload.service_name:
            score += 40

        historical_root_words = _keywords(historical.root_cause)
        if current_root_words and historical_root_words:
            union = current_root_words | historical_root_words
            overlap = current_root_words & historical_root_words
            score += round((len(overlap) / len(union)) * 30)

        historical_types = {value.value for value in historical.alert_types}
        if current_alert_types & historical_types:
            score += 20

        if historical.severity == payload.severity:
            score += 10

        if score > 0:
            matches.append(
                SimilarIncidentMatch(
                    **historical.model_dump(),
                    similarity_percentage=min(score, 100),
                )
            )

    matches.sort(
        key=lambda item: item.similarity_percentage,
        reverse=True,
    )
    return SimilarIncidentResponse(matches=matches)
