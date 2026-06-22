# YouTube Relay Bot — Claude Code Context

## What this project does
Downloads new videos from a source YouTube channel and re-uploads them to the owner's channel. Runs on OCI VM (me-jeddah-1) in Docker Compose with a Telegram bot as the control interface.

## Key files
- `src/pipeline.py` — orchestrates the full download → upload flow
- `src/downloader.py` — uses yt-dlp; tracks processed videos in `data/processed_videos.json`
- `src/uploader.py` — YouTube Data API v3 OAuth2 upload; token stored in `config/token.json`
- `src/telegram_bot.py` — bot handlers: /run /status /help + scheduled_relay callback
- `src/scheduler.py` — registers APScheduler daily jobs via telegram job_queue
- `src/config.py` — all config read from `.env`

## Deploy target
OCI VM, me-jeddah-1, `docker compose up -d`. First run requires interactive OAuth for YouTube.

## Secrets — never commit
- `.env` (all tokens)
- `config/token.json` (YouTube OAuth token)
- `config/client_secret.json` (Google OAuth credentials)

## Dev setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in values
python -m src.main
```
