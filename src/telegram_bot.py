import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from . import config
from .pipeline import run_relay

logger = logging.getLogger(__name__)


def _is_allowed(update: Update) -> bool:
    return update.effective_chat.id == config.TELEGRAM_ALLOWED_CHAT_ID


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_allowed(update):
        return
    await update.message.reply_text(
        "YouTube Relay Bot is running.\n\n"
        "Commands:\n"
        "/run   — trigger relay now\n"
        "/status — show last run summary\n"
        "/help  — this message"
    )


async def cmd_run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_allowed(update):
        return
    await update.message.reply_text("Starting relay pipeline...")
    try:
        summary = run_relay()
        text = (
            f"Relay complete:\n"
            f"  Found:    {summary['found']}\n"
            f"  Uploaded: {summary['uploaded']}\n"
            f"  Failed:   {summary['failed']}"
        )
    except Exception as e:
        text = f"Pipeline error: {e}"
        logger.exception("Manual relay failed")

    await update.message.reply_text(text)


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_allowed(update):
        return
    last = context.bot_data.get("last_summary")
    if not last:
        await update.message.reply_text("No run recorded yet.")
        return
    await update.message.reply_text(
        f"Last run summary:\n"
        f"  Found:    {last['found']}\n"
        f"  Uploaded: {last['uploaded']}\n"
        f"  Failed:   {last['failed']}"
    )


async def scheduled_relay(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Called by APScheduler via job_queue."""
    logger.info("Scheduled relay triggered")
    try:
        summary = run_relay()
        context.bot_data["last_summary"] = summary
        text = (
            f"Scheduled relay done:\n"
            f"  Found:    {summary['found']}\n"
            f"  Uploaded: {summary['uploaded']}\n"
            f"  Failed:   {summary['failed']}"
        )
    except Exception as e:
        text = f"Scheduled relay error: {e}"
        logger.exception("Scheduled relay failed")

    await context.bot.send_message(chat_id=config.TELEGRAM_ALLOWED_CHAT_ID, text=text)


def build_app() -> Application:
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_start))
    app.add_handler(CommandHandler("run", cmd_run))
    app.add_handler(CommandHandler("status", cmd_status))
    return app
