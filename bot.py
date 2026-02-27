"""
Telegram Auto-Acceptor Bot (Webhook Version for Render)
Uses python-telegram-bot v20+ (async API)
"""

import logging
import os
from flask import Flask, request
from telegram import Update, ChatMemberUpdated
from telegram.ext import (
    Application,
    ChatJoinRequestHandler,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
)
from config import BOT_TOKEN, WELCOME_MESSAGE, FAREWELL_MESSAGE, LOG_LEVEL

# ──────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# Flask App
# ──────────────────────────────────────────────
flask_app = Flask(__name__)

# ──────────────────────────────────────────────
# Helper
# ──────────────────────────────────────────────
def _format_message(template: str, user, chat) -> str:
    return template.format(
        first_name=user.first_name or "",
        last_name=user.last_name or "",
        username=f"@{user.username}" if user.username else "",
        chat_title=chat.title or "the chat",
    )

# ──────────────────────────────────────────────
# Handlers
# ──────────────────────────────────────────────
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 <b>Hello!</b>\n\n"
        "I automatically approve join requests and send welcome / farewell messages.",
        parse_mode="HTML",
    )

async def approve_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    join_request = update.chat_join_request
    user = join_request.from_user
    chat = join_request.chat

    try:
        await join_request.approve()
    except Exception as exc:
        logger.error("Failed to approve join request: %s", exc)
        return

    welcome_text = _format_message(WELCOME_MESSAGE, user, chat)
    try:
        await context.bot.send_message(
            chat_id=user.id,
            text=welcome_text,
            parse_mode="HTML",
        )
    except Exception as exc:
        logger.warning("Could not send welcome DM: %s", exc)

def _is_member_left(update: ChatMemberUpdated) -> bool:
    old = update.old_chat_member
    new = update.new_chat_member
    was_member = old.status in ("member", "administrator", "creator", "restricted")
    is_gone = new.status in ("left", "kicked", "banned")
    return was_member and is_gone

async def farewell(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_member_update = update.chat_member
    if chat_member_update is None:
        return

    if not _is_member_left(chat_member_update):
        return

    user = chat_member_update.new_chat_member.user
    chat = chat_member_update.chat

    farewell_text = _format_message(FAREWELL_MESSAGE, user, chat)
    try:
        await context.bot.send_message(
            chat_id=user.id,
            text=farewell_text,
            parse_mode="HTML",
        )
    except Exception as exc:
        logger.warning("Could not send farewell DM: %s", exc)

# ──────────────────────────────────────────────
# Create Telegram Application
# ──────────────────────────────────────────────
application = Application.builder().token(BOT_TOKEN).build()

application.add_handler(CommandHandler("start", start_command))
application.add_handler(ChatJoinRequestHandler(approve_join_request))
application.add_handler(ChatMemberHandler(farewell, ChatMemberHandler.CHAT_MEMBER))

# ──────────────────────────────────────────────
# Webhook Route
# ──────────────────────────────────────────────
@flask_app.post(f"/{BOT_TOKEN}")
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

@flask_app.get("/")
def home():
    return "Bot is running!"

# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 10000))

    # Set webhook URL
    RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")
    if not RENDER_EXTERNAL_URL:
        raise RuntimeError("RENDER_EXTERNAL_URL not set!")

    webhook_url = f"{RENDER_EXTERNAL_URL}/{BOT_TOKEN}"
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=webhook_url,
    )