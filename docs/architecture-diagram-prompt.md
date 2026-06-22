# Architecture Diagram — Image Generation Prompt

Use this prompt in **Gemini**, **Midjourney**, **DALL-E**, or any AI image generator to create the project architecture diagram.

---

## Prompt for Gemini / ChatGPT Image Generation

```
Create a clean, modern software architecture diagram for a project called "YouTube Relay Bot".

Layout: Left-to-right data flow with a vertical control panel on the right.

Components to include:

LEFT SIDE — Data Flow:
1. "Source YouTube Channel" — YouTube logo icon, labeled "Friend's Channel"
2. Arrow labeled "yt-dlp download"
3. "Downloader Service" — Python logo, cloud download icon
4. Arrow labeled "save temp file"
5. "Local Storage" — folder/disk icon, labeled "downloads/"
6. Arrow labeled "YouTube Data API v3"
7. "Uploader Service" — Python logo, upload icon
8. Arrow labeled "publish video"
9. "Target YouTube Channel" — YouTube logo icon, labeled "My Channel"

RIGHT SIDE — Control & Scheduling:
10. "APScheduler" — clock icon, labeled "6:00 AM / 6:00 PM Asia/Riyadh"
11. Arrow from APScheduler to Downloader labeled "trigger"
12. "Telegram Bot" — Telegram logo, labeled "/run /status /help"
13. Two-way arrow between Telegram Bot and a "User / Phone" icon
14. Arrow from Telegram Bot to Downloader labeled "manual trigger"
15. Arrow from Uploader to Telegram Bot labeled "notifications"

BOTTOM — Infrastructure:
16. A rounded rectangle around all components labeled "OCI VM — me-jeddah-1 (Always Free)"
17. Inside that, a Docker whale icon labeled "Docker Compose"

OPTIONAL — Top right corner:
18. Small "Gemini AI" icon labeled "Optional: title translation (free tier)"

Style:
- Dark background (#1a1a2e or similar deep navy)
- Accent colors: YouTube red (#FF0000), Telegram blue (#2CA5E0), Python yellow (#FFD43B)
- Clean sans-serif font (Inter or similar)
- Rounded rectangles for services
- Directional arrows with labels
- Professional technical diagram style, not hand-drawn
- 1920x1080 or 16:9 aspect ratio
```

---

## Shorter Prompt (if the above is too long)

```
Technical architecture diagram, dark theme navy background:
- Left: "Source YouTube Channel" → yt-dlp Downloader → Local Storage → YouTube API Uploader → "Target YouTube Channel"
- Right: APScheduler (clock, 6AM/6PM) triggers the pipeline; Telegram Bot (blue) handles /run /status commands and sends notifications
- Bottom: all wrapped in "OCI VM Docker Compose" box
- Icons: YouTube red, Telegram blue, Python yellow
- Style: clean modern tech diagram, 16:9
```
