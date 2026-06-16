from sqlalchemy.orm import Session

from app.models.normalized_alert import NormalizedAlert
from app.models.raw_alert import RawAlert
from app.schemas.alert_schema import NormalizedAlertCreate


def store_raw_alert(
    db: Session,
    alert_id: str,
    source: str,
    payload: dict,
    project_id: str | None = None,
) -> RawAlert:
    raw_alert = RawAlert(
        alert_id=alert_id,
        project_id=project_id,
        source=source,
        raw_payload=payload,
    )
    db.add(raw_alert)
    db.commit()
    db.refresh(raw_alert)
    return raw_alert


def store_normalized_alert(db: Session, alert: NormalizedAlertCreate) -> NormalizedAlert:
    normalized_alert = NormalizedAlert(**alert.model_dump())
    db.add(normalized_alert)
    db.commit()
    db.refresh(normalized_alert)
    return normalized_alert


def get_alerts(db: Session, skip: int = 0, limit: int = 100) -> list[NormalizedAlert]:
    return (
        db.query(NormalizedAlert)
        .order_by(NormalizedAlert.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_normalized_alert_by_alert_id(db: Session, alert_id: str) -> NormalizedAlert | None:
    return db.query(NormalizedAlert).filter(NormalizedAlert.alert_id == alert_id).first()


def get_alert_by_alert_id(db: Session, alert_id: str) -> NormalizedAlert | None:
    return get_normalized_alert_by_alert_id(db, alert_id)


def get_raw_alert_by_alert_id(db: Session, alert_id: str) -> RawAlert | None:
    return db.query(RawAlert).filter(RawAlert.alert_id == alert_id).first()
