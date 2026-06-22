# YouTube Relay Bot

Automated pipeline that downloads new videos from a source YouTube channel and re-uploads them to a target channel. Controlled via a Telegram bot with scheduled runs at 6 AM and 6 PM (Asia/Riyadh).

## Features

- Scheduled relay twice daily (6 AM & 6 PM, configurable)
- Telegram bot for manual trigger, status checks, and notifications
- Keeps original video title and description + adds source credit
- Tracks processed videos — no duplicates
- Runs 24/7 on OCI VM via Docker Compose
- Optional Gemini AI integration (free tier) for title/description translation

## Architecture

```
Source YouTube Channel
        │
        ▼
   [yt-dlp Downloader]
        │
        ▼
  Local Temp Storage
        │
        ▼
  [YouTube API Uploader]
        │
        ▼
Target YouTube Channel

[APScheduler] ──── triggers at 6AM / 6PM (Asia/Riyadh)
[Telegram Bot] ──── /run  /status  /help  + notifications

All running on OCI VM (me-jeddah-1) via Docker Compose
```

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-org/youtube-relay-bot.git
cd youtube-relay-bot
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and fill in your values
```

### 3. Get a Telegram Bot Token

1. Open Telegram → talk to [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow instructions
3. Copy the token into `.env` → `TELEGRAM_BOT_TOKEN`
4. Get your Chat ID: talk to [@userinfobot](https://t.me/userinfobot) → `TELEGRAM_ALLOWED_CHAT_ID`

### 4. Get YouTube Data API credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project → Enable **YouTube Data API v3**
3. Create OAuth 2.0 credentials (Desktop app)
4. Download `client_secret.json` → place in `config/`
5. First run will open a browser for OAuth consent — do this once on the OCI VM

### 5. Deploy on OCI VM

```bash
# Copy files to OCI VM
scp -r . opc@<your-oci-ip>:~/youtube-relay-bot/

# SSH into VM
ssh opc@<your-oci-ip>

# Run
cd ~/youtube-relay-bot
docker compose up -d

# First-time OAuth (run interactively once)
docker compose run --rm relay-bot python -c "from src.uploader import _get_credentials; _get_credentials()"
```

### 6. Check logs

```bash
docker compose logs -f
# or
tail -f logs/relay.log
```

## Telegram Commands

| Command | Description |
|---------|-------------|
| `/run`  | Trigger relay pipeline immediately |
| `/status` | Show last run summary |
| `/help` | Show available commands |

## Optional: Gemini AI

Enable in `.env`:

```env
GEMINI_API_KEY=your_key_here
GEMINI_ENABLED=true
```

Get a free API key at [aistudio.google.com](https://aistudio.google.com). Free tier: 15 requests/min, 1M tokens/day.

When enabled, Gemini can translate video titles/descriptions to Arabic.

## Project Structure

```
youtube-relay-bot/
├── src/
│   ├── main.py          # Entry point
│   ├── config.py        # Environment config
│   ├── downloader.py    # yt-dlp wrapper
│   ├── uploader.py      # YouTube API v3 uploader
│   ├── pipeline.py      # Orchestrates download → upload
│   ├── scheduler.py     # APScheduler jobs (6AM/6PM)
│   └── telegram_bot.py  # Telegram bot handlers
├── config/
│   └── config.yaml      # App configuration
├── .env.example         # Environment template
├── Dockerfile
└── docker-compose.yml
```

## License

Internal use only.
