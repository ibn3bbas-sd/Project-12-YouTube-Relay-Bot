import logging

from telegram.ext import Application

from . import config
from .telegram_bot import scheduled_relay

logger = logging.getLogger(__name__)


def _parse_time(time_str: str) -> tuple[int, int]:
    h, m = time_str.split(":")
    return int(h), int(m)


def register_jobs(app: Application) -> None:
    morning_h, morning_m = _parse_time(config.SCHEDULE_MORNING)
    evening_h, evening_m = _parse_time(config.SCHEDULE_EVENING)

    app.job_queue.run_daily(
        scheduled_relay,
        time=__import__("datetime").time(
            morning_h, morning_m, tzinfo=__import__("zoneinfo").ZoneInfo(config.TIMEZONE)
        ),
        name="relay_morning",
    )

    app.job_queue.run_daily(
        scheduled_relay,
        time=__import__("datetime").time(
            evening_h, evening_m, tzinfo=__import__("zoneinfo").ZoneInfo(config.TIMEZONE)
        ),
        name="relay_evening",
    )

    logger.info(
        "Scheduled relay at %s and %s (%s)",
        config.SCHEDULE_MORNING,
        config.SCHEDULE_EVENING,
        config.TIMEZONE,
    )
