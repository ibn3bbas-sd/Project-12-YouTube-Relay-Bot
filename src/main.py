import logging
import os

from .scheduler import register_jobs
from .telegram_bot import build_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/relay.log"),
    ],
)

logger = logging.getLogger(__name__)


def main() -> None:
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("downloads", exist_ok=True)

    app = build_app()
    register_jobs(app)

    logger.info("YouTube Relay Bot started")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
