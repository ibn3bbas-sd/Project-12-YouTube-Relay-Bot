import logging
import os

from . import config, downloader, uploader

logger = logging.getLogger(__name__)


def run_relay() -> dict:
    """Full pipeline: fetch → download → upload → cleanup. Returns a summary dict."""
    summary = {"found": 0, "uploaded": 0, "failed": 0, "skipped": 0}

    videos = downloader.fetch_new_videos(config.SOURCE_CHANNEL_ID)
    summary["found"] = len(videos)

    if not videos:
        logger.info("No new videos to relay.")
        return summary

    for video in videos:
        logger.info("Processing: %s", video["title"])
        file_path = downloader.download_video(video)

        if not file_path:
            summary["failed"] += 1
            downloader.mark_processed(video["id"])  # skip permanently on download failure
            continue

        video_id = uploader.upload_video(file_path, video)

        if video_id:
            summary["uploaded"] += 1
            downloader.mark_processed(video["id"])
        else:
            summary["failed"] += 1

        if not config.GEMINI_ENABLED or True:  # cleanup always unless debugging
            try:
                os.remove(file_path)
                logger.debug("Deleted temp file: %s", file_path)
            except OSError:
                pass

    return summary
