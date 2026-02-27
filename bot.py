"""
Telegram Auto-Acceptor Bot
===========================
Automatically approves all join requests, sends welcome DMs,
and posts farewell messages when members leave.

Uses python-telegram-bot v20+ (async API).
"""

import logging
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
#  Logging
# ──────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
#  Helper: format a message template
# ──────────────────────────────────────────────
def _format_message(template: str, user, chat) -> str:
    """Replace placeholders in a message template."""
    return template.format(
        first_name=user.first_name or "",
        last_name=user.last_name or "",
        username=f"@{user.username}" if user.username else "",
        chat_title=chat.title or "the chat",
    )


# ──────────────────────────────────────────────
#  /start command
# ──────────────────────────────────────────────
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond to the /start command in DM."""
    await update.message.reply_text(
        "👋 <b>Hello!</b>\n\n"
        "I automatically approve join requests and send welcome / farewell messages.\n"
        "Add me as an <b>admin</b> in your channel or group to get started!",
        parse_mode="HTML",
    )


# ──────────────────────────────────────────────
#  Auto-approve join requests + welcome DM
# ──────────────────────────────────────────────
async def approve_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Approve every incoming join request and DM the user a welcome message."""
    join_request = update.chat_join_request
    user = join_request.from_user
    chat = join_request.chat

    # 1) Approve the request
    try:
        await join_request.approve()
        logger.info(
            "Approved join request from %s (id=%s) for chat '%s'",
            user.first_name,
            user.id,
            chat.title,
        )
    except Exception as exc:
        logger.error("Failed to approve join request: %s", exc)
        return

    # 2) Send a welcome DM to the user
    welcome_text = _format_message(WELCOME_MESSAGE, user, chat)
    try:
        await context.bot.send_message(
            chat_id=user.id,
            text=welcome_text,
            parse_mode="HTML",
        )
        logger.info("Sent welcome DM to %s (id=%s)", user.first_name, user.id)
    except Exception as exc:
        # The user might have blocked the bot or never started it,
        # so DM delivery can fail — that's okay.
        logger.warning(
            "Could not send welcome DM to %s (id=%s): %s",
            user.first_name,
            user.id,
            exc,
        )


# ──────────────────────────────────────────────
#  Detect when a member leaves → farewell
# ──────────────────────────────────────────────
def _is_member_left(update: ChatMemberUpdated) -> bool:
    """Return True if the update represents a member leaving."""
    old = update.old_chat_member
    new = update.new_chat_member

    # Was a member (or admin/owner/restricted) and is now left/kicked/banned
    was_member = old.status in ("member", "administrator", "creator", "restricted")
    is_gone = new.status in ("left", "kicked", "banned")
    return was_member and is_gone


async def farewell(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a farewell DM to the user when they leave the group/channel."""
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
        logger.info(
            "Sent farewell DM to %s (id=%s) after leaving '%s'",
            user.first_name,
            user.id,
            chat.title,
        )
    except Exception as exc:
        # The user might have blocked the bot or never started it
        logger.warning(
            "Could not send farewell DM to %s (id=%s): %s",
            user.first_name,
            user.id,
            exc,
        )


# ──────────────────────────────────────────────
#  Main entry point
# ──────────────────────────────────────────────
def main() -> None:
    """Build the application, register handlers, and start polling."""
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error(
            "Bot token not set! Edit config.py or set the BOT_TOKEN environment variable."
        )
        return

    app = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(ChatJoinRequestHandler(approve_join_request))
    app.add_handler(ChatMemberHandler(farewell, ChatMemberHandler.CHAT_MEMBER))

    logger.info("Bot is starting… Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
