# 🤖 Telegram Auto-Acceptor Bot

Automatically **approves all join requests**, sends a **welcome DM**, and posts a **farewell message** when members leave your Telegram channel or group.

---

## 📋 Prerequisites

- **Python 3.9+**
- A Telegram bot token from [**@BotFather**](https://t.me/BotFather)

---

## 🚀 Quick Setup

### 1. Create Your Bot

1. Open Telegram and search for **@BotFather**.
2. Send `/newbot` and follow the prompts.
3. Copy the **API token** you receive.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Token

Open **`config.py`** and replace `YOUR_BOT_TOKEN_HERE` with your token:

```python
BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
```

Or set it as an environment variable:

```bash
# Linux / macOS
export BOT_TOKEN="your-token-here"

# Windows (PowerShell)
$env:BOT_TOKEN = "your-token-here"
```

### 4. Add the Bot to Your Channel / Group

1. Go to your channel/group **Settings → Administrators**.
2. Add the bot as an **admin** with at least these permissions:
   - ✅ **Invite Users via Link** (to approve join requests)
   - ✅ **Post Messages** (to send farewell messages in the chat)
3. Enable **Join Requests** on your channel/group (Settings → Invite Links → Request Admin Approval).

### 5. Run the Bot

```bash
python bot.py
```

You should see: `Bot is starting… Press Ctrl+C to stop.`

---

## ✏️ Customize Messages

Edit the templates in **`config.py`**. Available placeholders:

| Placeholder    | Description                       |
| -------------- | --------------------------------- |
| `{first_name}` | User's first name                 |
| `{last_name}`  | User's last name (may be empty)   |
| `{username}`   | User's @username (may be empty)   |
| `{chat_title}` | Name of the channel / group       |

Messages support **HTML formatting** (`<b>`, `<i>`, `<code>`, `<a href="...">`, etc.).

---

## 📁 Project Structure

```
vs auto acceptor bot/
├── bot.py              # Main bot logic
├── config.py           # Token & message templates
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## ⚠️ Notes

- The **welcome DM** will only work if the user has **started the bot** (sent `/start`) at least once. This is a Telegram API limitation — bots cannot DM users who haven't interacted with them first.
- The **farewell handler** requires the bot to receive `chat_member` updates. The code uses `allowed_updates=Update.ALL_TYPES` to ensure this.
- If you're running on a server, consider using a process manager like **systemd** or **PM2** to keep the bot running.
