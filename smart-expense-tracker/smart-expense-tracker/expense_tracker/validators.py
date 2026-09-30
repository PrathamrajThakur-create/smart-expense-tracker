"""Input validation. Every parser raises ValidationError with a friendly message."""
import math
from datetime import date, datetime

from .models import CATEGORIES


class ValidationError(ValueError):
    """Raised when user input is invalid."""


def parse_amount(raw) -> float:
    try:
        value = float(str(raw).strip())
    except ValueError:
        raise ValidationError("Amount must be a number.") from None
    if not math.isfinite(value) or value <= 0:
        raise ValidationError("Amount must be greater than zero.")
    return round(value, 2)


def parse_date(raw, today: date = None) -> str:
    today = today or date.today()
    raw = (raw or "").strip()
    if not raw:
        return today.isoformat()
    try:
        parsed = datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        raise ValidationError("Date must be in YYYY-MM-DD format.") from None
    if parsed > today:
        raise ValidationError("Date cannot be in the future.")
    return parsed.isoformat()


def parse_category(raw) -> str:
    cleaned = (raw or "").strip().title()
    if cleaned not in CATEGORIES:
        raise ValidationError("Category must be one of: " + ", ".join(CATEGORIES))
    return cleaned


def parse_description(raw) -> str:
    text = (raw or "").strip()
    if not text:
        raise ValidationError("Description cannot be empty.")
    return text[:80]


def parse_month(raw, today: date = None) -> str:
    today = today or date.today()
    raw = (raw or "").strip()
    if not raw:
        return today.strftime("%Y-%m")
    try:
        return datetime.strptime(raw, "%Y-%m").strftime("%Y-%m")
    except ValueError:
        raise ValidationError("Month must be in YYYY-MM format.") from None
