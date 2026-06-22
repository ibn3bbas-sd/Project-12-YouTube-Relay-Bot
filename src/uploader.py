import logging
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from . import config

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def _get_credentials() -> Credentials:
    creds = None

    if os.path.exists(config.YOUTUBE_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(config.YOUTUBE_TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config.YOUTUBE_CLIENT_SECRET_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        os.makedirs(os.path.dirname(config.YOUTUBE_TOKEN_FILE), exist_ok=True)
        with open(config.YOUTUBE_TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return creds


def upload_video(file_path: str, video_meta: dict) -> str | None:
    """Upload video to target channel. Returns YouTube video ID or None on failure."""
    creds = _get_credentials()
    youtube = build("youtube", "v3", credentials=creds)

    source_credit = (
        f"\n\n---\nOriginal video by: {video_meta.get('channel_name', '')}\n"
        f"{video_meta.get('url', '')}"
    )

    body = {
        "snippet": {
            "title": video_meta["title"],
            "description": (video_meta.get("description") or "") + source_credit,
            "categoryId": "22",
        },
        "status": {
            "privacyStatus": "public",
        },
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype="video/mp4")

    try:
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                logger.info("Upload progress: %d%%", int(status.progress() * 100))

        video_id = response["id"]
        logger.info("Uploaded '%s' → https://youtu.be/%s", video_meta["title"], video_id)
        return video_id

    except Exception as e:
        logger.error("Upload failed for '%s': %s", video_meta["title"], e)
        return None
