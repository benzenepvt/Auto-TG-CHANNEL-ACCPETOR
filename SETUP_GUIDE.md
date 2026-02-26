# 📖 Complete Setup Guide — Telegram Auto-Acceptor Bot

A step-by-step guide to set up the bot **from scratch**, even if you've never worked with Python or Telegram bots before.

---

## Table of Contents

1. [Install Python](#1--install-python)
2. [Download the Project](#2--download-the-project)
3. [Create a Virtual Environment (Optional but Recommended)](#3--create-a-virtual-environment)
4. [Install Dependencies](#4--install-dependencies)
5. [Create Your Telegram Bot via BotFather](#5--create-your-telegram-bot-via-botfather)
6. [Configure the Bot Token (.env file)](#6--configure-the-bot-token)
7. [Customize Welcome & Farewell Messages](#7--customize-welcome--farewell-messages)
8. [Set Up Your Channel / Group](#8--set-up-your-channel--group)
9. [Run the Bot](#9--run-the-bot)
10. [Test Everything](#10--test-everything)
11. [Keep the Bot Running 24/7 (Optional)](#11--keep-the-bot-running-247)
12. [Troubleshooting](#12--troubleshooting)

---

## 1 — Install Python

You need **Python 3.9 or higher**.

### Windows

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python installer.
3. **Important:** Check the box that says **"Add Python to PATH"** during installation.
4. Click **Install Now**.
5. Verify the installation by opening **Command Prompt** or **PowerShell** and running:

   ```bash
   python --version
   ```

   You should see something like `Python 3.12.x`.

### macOS / Linux

```bash
# macOS (Homebrew)
brew install python

# Ubuntu / Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# Verify
python3 --version
```

---

## 2 — Download the Project

If you received this as a folder, you're all set. The project folder should contain:

```
vs auto acceptor bot/
├── bot.py              # Main bot code
├── config.py           # Configuration loader
├── .env                # Your secret token (edit this!)
├── requirements.txt    # Python dependencies
├── README.md           # Quick overview
└── SETUP_GUIDE.md      # This file
```

---

## 3 — Create a Virtual Environment

A virtual environment keeps your project's dependencies separate from your system Python. This is **optional** but strongly recommended.

### Windows (PowerShell)

```powershell
# Navigate to the project folder
cd "c:\Users\hp\Desktop\New folder (2)\vs auto acceptor bot"

# Create a virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate

# You should now see (venv) at the beginning of your prompt
```

### macOS / Linux

```bash
cd "/path/to/vs auto acceptor bot"
python3 -m venv venv
source venv/bin/activate
```

> **Tip:** You need to activate the venv every time you open a new terminal to run the bot.

---

## 4 — Install Dependencies

With your terminal open in the project folder (and venv activated, if you created one):

```bash
pip install -r requirements.txt
```

This installs:
- `python-telegram-bot` — the Telegram Bot API wrapper
- `python-dotenv` — loads your `.env` file automatically

---

## 5 — Create Your Telegram Bot via BotFather

1. Open Telegram and search for **@BotFather** (or go to [t.me/BotFather](https://t.me/BotFather)).
2. Send the command:
   ```
   /newbot
   ```
3. BotFather will ask you for a **name** for the bot (e.g., `My Auto Acceptor`).
4. Then it will ask for a **username** (must end with `bot`, e.g., `my_auto_acceptor_bot`).
5. BotFather will reply with your **bot token**, which looks like this:
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
6. **Copy this token** — you'll need it in the next step.

> ⚠️ **Keep your token secret!** Anyone with this token can control your bot.

### Optional: Disable Group Privacy Mode

By default, bots in groups only see commands and messages that mention them. To ensure the bot receives **all updates** (including member join/leave events):

1. In BotFather, send:
   ```
   /mybots
   ```
2. Select your bot → **Bot Settings** → **Group Privacy** → **Turn off**.

---

## 6 — Configure the Bot Token

Open the **`.env`** file in any text editor and replace `YOUR_BOT_TOKEN_HERE` with your actual token:

**Before:**
```env
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
```

**After:**
```env
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

Save the file. That's it — the bot will automatically read this file when it starts.

> **Alternative:** You can also set the token as a system environment variable instead of using the `.env` file.

---

## 7 — Customize Welcome & Farewell Messages

Open **`config.py`** to edit the messages. You'll see two templates:

### Welcome Message (sent as DM to the user)

```python
WELCOME_MESSAGE = (
    "🎉 <b>Welcome, {first_name}!</b>\n\n"
    "Your request to join <b>{chat_title}</b> has been approved.\n"
    "We're glad to have you here! Feel free to explore and enjoy. 🚀"
)
```

### Farewell Message (sent in the group/channel)

```python
FAREWELL_MESSAGE = (
    "👋 <b>{first_name}</b> has left <b>{chat_title}</b>.\n"
    "We'll miss you! Goodbye and take care. 💙"
)
```

### Available Placeholders

| Placeholder    | Description                     | Example        |
| -------------- | ------------------------------- | -------------- |
| `{first_name}` | User's first name               | `John`         |
| `{last_name}`  | User's last name (may be empty) | `Doe`          |
| `{username}`   | User's @username                | `@johndoe`     |
| `{chat_title}` | Channel / group name            | `My Channel`   |

### Supported HTML Tags

Messages support Telegram's HTML formatting:
- `<b>bold</b>`
- `<i>italic</i>`
- `<u>underline</u>`
- `<s>strikethrough</s>`
- `<code>inline code</code>`
- `<a href="https://example.com">link</a>`

---

## 8 — Set Up Your Channel / Group

### Step A: Add the Bot as Admin

1. Open your **channel** or **group** in Telegram.
2. Go to **Settings** (tap the channel/group name at the top).
3. Go to **Administrators** → **Add Administrator**.
4. Search for your bot by its username and add it.
5. Grant these **permissions**:

   | Permission          | Required? | Why                              |
   | ------------------- | --------- | -------------------------------- |
   | Invite Users        | ✅ Yes    | Needed to approve join requests  |
   | Post Messages       | ✅ Yes    | Needed to send farewell messages |
   | Other permissions   | ❌ No     | Not needed, leave unchecked      |

6. Save.

### Step B: Enable Join Requests

1. In the channel/group **Settings**, go to **Invite Links**.
2. Create a new invite link (or edit the primary one).
3. Enable **"Request Admin Approval"** (sometimes called "Join Requests").
4. Save the link.

Now anyone who clicks this link will need to be approved — and the bot will auto-approve them!

---

## 9 — Run the Bot

Open your terminal in the project folder and run:

```bash
python bot.py
```

You should see output like:

```
2026-02-11 20:30:00,000 - __main__ - INFO - Bot is starting… Press Ctrl+C to stop.
```

The bot is now **running and listening** for events. Keep this terminal window open.

To stop the bot, press **Ctrl + C**.

---

## 10 — Test Everything

### Test Auto-Approval + Welcome DM

1. From a **different Telegram account** (or ask a friend), send `/start` to your bot first (this allows the bot to DM them).
2. Have them click the **join request link** for your channel/group.
3. The bot should:
   - ✅ **Auto-approve** the request instantly
   - ✅ **Send a welcome DM** to the user

### Test Farewell Message

1. Have the same person **leave** the group/channel.
2. The bot should:
   - ✅ **Post a farewell message** in the group/channel

### Check the Bot's Terminal

You'll see logs like:

```
INFO - Approved join request from John (id=12345678) for chat 'My Channel'
INFO - Sent welcome DM to John (id=12345678)
INFO - Sent farewell message for John (id=12345678) in chat 'My Channel'
```

---

## 11 — Keep the Bot Running 24/7

If you close the terminal, the bot stops. To keep it running, you have a few options:

### Option A: Run on a VPS / Cloud Server

Deploy on a cheap VPS (like DigitalOcean, Hetzner, or Oracle Cloud Free Tier) and use:

```bash
# Using nohup (simple)
nohup python bot.py &

# Using screen
screen -S bot
python bot.py
# Press Ctrl+A, then D to detach
```

### Option B: Use systemd (Linux)

Create a service file at `/etc/systemd/system/telegram-bot.service`:

```ini
[Unit]
Description=Telegram Auto-Acceptor Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/vs auto acceptor bot
ExecStart=/path/to/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

### Option C: Keep it Running on Windows

Use **Task Scheduler** or simply keep the terminal open. For a more robust solution, consider using [NSSM](https://nssm.cc/) to run it as a Windows service.

---

## 12 — Troubleshooting

### ❌ "Bot token not set!"

You forgot to add your token. Open `.env` and paste your token after `BOT_TOKEN=`.

### ❌ Welcome DM not received

The user must have **sent `/start` to the bot** at least once before the bot can DM them. This is a Telegram API restriction — bots cannot message users who haven't interacted with them first.

**Workaround:** In your join request link's description, ask users to start the bot first.

### ❌ Farewell message not appearing

- Make sure the bot has **Post Messages** permission in the group.
- For **channels** (not groups), farewell detection may not work because Telegram doesn't send `chat_member` updates for channels in the same way. This works best in **groups** and **supergroups**.

### ❌ "ModuleNotFoundError: No module named 'telegram'"

You haven't installed the dependencies. Run:

```bash
pip install -r requirements.txt
```

If using a virtual environment, make sure it's **activated** first.

### ❌ "ModuleNotFoundError: No module named 'dotenv'"

Same as above — run `pip install -r requirements.txt`.

### ❌ Bot doesn't auto-approve

- Ensure the bot is an **admin** with **Invite Users** permission.
- Ensure **Join Requests** are enabled on the invite link.
- Check the terminal for error messages.

---

## 📁 File Overview

| File               | What It Does                                        |
| ------------------ | --------------------------------------------------- |
| `bot.py`           | Main bot logic — handlers for join, leave, /start   |
| `config.py`        | Loads settings from `.env` + message templates      |
| `.env`             | Your secret bot token (never share this!)           |
| `requirements.txt` | Python packages to install                          |
| `README.md`        | Quick project overview                              |
| `SETUP_GUIDE.md`   | This detailed guide                                 |

---

**🎉 You're all set! Your bot is now auto-approving members, welcoming them, and saying farewell when they leave.**
