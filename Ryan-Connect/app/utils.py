from datetime import datetime, timezone

def toisoformat(value):
    """Convert datetime to ISO format string."""
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.isoformat()
    return value