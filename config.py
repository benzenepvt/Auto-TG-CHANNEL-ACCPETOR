"""
Configuration for the Telegram Auto-Acceptor Bot.
Edit the values below or set them in the .env file.
"""

import os
from dotenv import load_dotenv

# Load variables from .env file (if it exists)
load_dotenv()

# ──────────────────────────────────────────────
#  BOT TOKEN  (get from @BotFather on Telegram)
# ──────────────────────────────────────────────
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# ──────────────────────────────────────────────
#  WELCOME MESSAGE
#  Sent as a DM to the user after their join
#  request is approved.
#  Placeholders:
#    {first_name}  - User's first name
#    {last_name}   - User's last name (may be empty)
#    {username}    - User's @username (may be empty)
#    {chat_title}  - Name of the channel / group
# ──────────────────────────────────────────────
WELCOME_MESSAGE = (
    "🎉 <b>Welcome, {first_name}!</b>\n\n"
    "Your request to join <b>{chat_title}</b> has been approved.\n"
    "We're glad to have you here! Feel free to explore and enjoy. 🚀"
)

# ──────────────────────────────────────────────
#  FAREWELL MESSAGE
#  Sent in the group/channel when a member leaves.
#  Placeholders:
#    {first_name}  - User's first name
#    {last_name}   - User's last name (may be empty)
#    {username}    - User's @username (may be empty)
#    {chat_title}  - Name of the channel / group
# ──────────────────────────────────────────────
FAREWELL_MESSAGE = (
    "👋 <b>{first_name}</b> has left <b>{chat_title}</b>.\n"
    "We'll miss you! Goodbye and take care. 💙"
)

# ──────────────────────────────────────────────
#  LOGGING LEVEL  (DEBUG, INFO, WARNING, ERROR)
# ──────────────────────────────────────────────
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
