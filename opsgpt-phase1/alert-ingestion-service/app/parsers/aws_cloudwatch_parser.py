from app.parsers.universal_alert_parser import parse_universal_alert


def parse_aws_cloudwatch_alert(payload: dict, fallback_alert_id: str | None = None) -> dict:
    return parse_universal_alert(payload, "aws_cloudwatch", fallback_alert_id, "aws_cloudwatch_parser")
