"""
====================================================
🤖 GitHub Super Telegram Bot
----------------------------------------------------
👨‍💻 Developer : SANJIT CHAURASIYA
📱 Telegram  : @SANJIT_CHAURASIYA
🛠️ Purpose  : GitHub Analysis via Telegram
⚠️ License  : Educational & Open Source

⚡ DO NOT REMOVE THIS WATERMARK
====================================================
"""

import logging
import html
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from github import Github, GithubException

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
GITHUB_TOKEN = None  # Optional but recommended

g = Github(GITHUB_TOKEN) if GITHUB_TOKEN else Github()

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ==========================================
# 🔍 SEARCH REPOS
# ==========================================
async def search_repos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /search <query>")
        return
    query = " ".join(context.args)
    results = g.search_repositories(query=query, sort="stars", order="desc")
    msg = f"<b>🔍 Results for {html.escape(query)}</b>\n\n"
    for repo in results[:5]:
        msg += f"⭐ <a href='{repo.html_url}'>{html.escape(repo.full_name)}</a>\n"
    await update.message.reply_text(msg, parse_mode="HTML", disable_web_page_preview=True)

# ==========================================
# 👤 USER INFO
# ==========================================
async def get_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = g.get_user(context.args[0])
    msg = (
        f"<b>👤 {html.escape(user.login)}</b>\n"
        f"Followers: {user.followers}\n"
        f"Repos: {user.public_repos}\n"
        f"<a href='{user.html_url}'>Profile</a>"
    )
    await update.message.reply_text(msg, parse_mode="HTML")

# ==========================================
# 📂 REPO DETAILS
# ==========================================
async def get_repo_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo = g.get_repo(context.args[0])
    msg = (
        f"<b>{html.escape(repo.full_name)}</b>\n"
        f"⭐ {repo.stargazers_count}\n"
        f"🍴 {repo.forks_count}\n"
        f"🐞 {repo.open_issues_count}\n"
        f"🗣️ {repo.language}"
    )
    await update.message.reply_text(msg, parse_mode="HTML")

# ==========================================
# 🆕 ADDITIONAL FEATURES
# ==========================================
async def stats(update, context):
    repo = g.get_repo(context.args[0])
    await update.message.reply_text(
        f"⭐ {repo.stargazers_count}\n🍴 {repo.forks_count}\n👁️ {repo.subscribers_count}"
    )

async def languages(update, context):
    repo = g.get_repo(context.args[0])
    msg = "<b>Languages</b>\n"
    for k in repo.get_languages():
        msg += f"- {k}\n"
    await update.message.reply_text(msg, parse_mode="HTML")

async def commits(update, context):
    repo = g.get_repo(context.args[0])
    msg = "<b>Recent Commits</b>\n"
    for c in repo.get_commits()[:5]:
        msg += f"- {html.escape(c.commit.message[:60])}\n"
    await update.message.reply_text(msg, parse_mode="HTML")

async def rate_limit(update, context):
    rate = g.get_rate_limit().core
    await update.message.reply_text(f"Remaining: {rate.remaining}")

async def ping(update, context):
    await update.message.reply_text("🏓 Pong! Bot is Alive")

async def about(update, context):
    await update.message.reply_text(
        "👨‍💻 Developed by SANJIT CHAURASIYA\n"
        "📱 Telegram: @SANJIT_CHAURASIYA\n"
        "🤖 GitHub Super Bot"
    )

# ==========================================
# 🤖 START / HELP
# ==========================================
async def start(update, context):
    await update.message.reply_text(
        "🤖 GitHub Super Bot\nUse /help to see commands"
    )

# ==========================================
# 🚀 BOT RUNNER
# ==========================================
if __name__ == "__main__":
    print("✅ GitHub Bot Running | Developed by SANJIT CHAURASIYA")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("search", search_repos))
    app.add_handler(CommandHandler("user", get_user))
    app.add_handler(CommandHandler("repo", get_repo_details))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("languages", languages))
    app.add_handler(CommandHandler("commits", commits))
    app.add_handler(CommandHandler("rate_limit", rate_limit))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("about", about))

    app.run_polling()
