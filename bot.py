from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import requests

# دریافت API Key از متغیر محیطی
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! نام فیلم مورد نظر را ارسال کنید.")

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()

    # درخواست به TMDb API برای جستجوی فیلم
    response = requests.get(
        f"{TMDB_BASE_URL}/search/movie",
        params={"api_key": TMDB_API_KEY, "query": query, "language": "fa-IR"}
    )
    if response.status_code != 200:
        await update.message.reply_text("⛔ خطا در ارتباط با TMDb API.")
        return

    data = response.json()
    if not data["results"]:
        await update.message.reply_text("❌ فیلم مورد نظر پیدا نشد.")
        return

    # دریافت اطلاعات اولین نتیجه
    movie = data["results"][0]
    title = movie["title"]
    description = movie["overview"]
    release_date = movie["release_date"] if "release_date" in movie else "نامشخص"
    poster_path = movie["poster_path"]

    # ساخت لینک‌های کیفیت فرضی
    base_download_url = "https://pl.ortatv.fun"
    links = (
        f"📥 [480p]({base_download_url}/{title.replace(' ', '_')}-480p.mp4)\n"
        f"📥 [720p]({base_download_url}/{title.replace(' ', '_')}-720p.mp4)\n"
        f"📥 [1080p]({base_download_url}/{title.replace(' ', '_')}-1080p.mp4)"
    )

    # ساخت پیام نهایی
    message = (
        f"🎬 *{title}*\n\n"
        f"📖 توضیحات: {description}\n"
        f"🗓 تاریخ انتشار: {release_date}\n\n"
        f"⬇️ لینک‌های دانلود:\n{links}"
    )

    # ارسال پیام به کاربر
    if poster_path:
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        await update.message.reply_photo(poster_url, caption=message, parse_mode="Markdown", disable_web_page_preview=True)
    else:
        await update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)

if __name__ == "__main__":
    # دریافت توکن ربات از متغیر محیطی
    token = os.getenv("BOT_TOKEN")

    # اجرای ربات
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    app.run_polling()
