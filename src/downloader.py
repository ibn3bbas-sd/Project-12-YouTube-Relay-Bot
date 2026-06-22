import json
import logging
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yt_dlp

from . import config

logger = logging.getLogger(__name__)


def _load_processed() -> set:
    if not os.path.exists(config.PROCESSED_FILE):
        return set()
    with open(config.PROCESSED_FILE) as f:
        return set(json.load(f))


def _save_processed(video_ids: set) -> None:
    os.makedirs(config.DATA_DIR, exist_ok=True)
    with open(config.PROCESSED_FILE, "w") as f:
        json.dump(list(video_ids), f)


def fetch_new_videos(channel_id: str) -> list[dict]:
    """Return metadata for videos not yet processed, uploaded within MAX_VIDEO_AGE_DAYS."""
    processed = _load_processed()
    cutoff = datetime.now(timezone.utc) - timedelta(days=config.MAX_VIDEO_AGE_DAYS)

    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "playlistend": 20,
    }

    url = f"https://www.youtube.com/channel/{channel_id}/videos"
    new_videos = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        entries = info.get("entries", [])

    for entry in entries:
        video_id = entry.get("id")
        if not video_id or video_id in processed:
            continue

        upload_date_str = entry.get("upload_date", "")
        if upload_date_str:
            upload_date = datetime.strptime(upload_date_str, "%Y%m%d").replace(tzinfo=timezone.utc)
            if upload_date < cutoff:
                continue

        new_videos.append({
            "id": video_id,
            "title": entry.get("title", ""),
            "description": entry.get("description", ""),
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "channel_name": entry.get("channel", ""),
            "upload_date": upload_date_str,
            "thumbnail": entry.get("thumbnail", ""),
        })

    logger.info("Found %d new video(s) to process", len(new_videos))
    return new_videos


def download_video(video: dict) -> str | None:
    """Download video to DOWNLOAD_DIR. Returns local file path or None on failure."""
    os.makedirs(config.DOWNLOAD_DIR, exist_ok=True)

    output_template = os.path.join(config.DOWNLOAD_DIR, "%(id)s.%(ext)s")
    ydl_opts = {
        "format": config.VIDEO_QUALITY,
        "outtmpl": output_template,
        "quiet": False,
        "no_warnings": False,
        "merge_output_format": "mp4",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video["url"]])

        # Locate the downloaded file
        for f in Path(config.DOWNLOAD_DIR).glob(f"{video['id']}.*"):
            logger.info("Downloaded: %s → %s", video["title"], f)
            return str(f)

    except Exception as e:
        logger.error("Download failed for %s: %s", video["id"], e)

    return None


def mark_processed(video_id: str) -> None:
    processed = _load_processed()
    processed.add(video_id)
    _save_processed(processed)
