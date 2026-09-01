from datetime import timezone
from zoneinfo import ZoneInfo

ZAMBIA_TIMEZONE = ZoneInfo("Africa/Lusaka")


def format_zambia_time(value):
    if value is None:
        return ""

    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    else:
        value = value.astimezone(timezone.utc)

    return value.astimezone(ZAMBIA_TIMEZONE).strftime(
        "%d/%m/%Y, %H:%M"
    )
