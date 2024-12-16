from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# اطلاعات فیلم "Inception" (اطلاعات فرضی)
MOVIE_DATA = {
    "Inception": {
        "title": "Inception",
        "description": "یک فیلم علمی تخیلی در مورد ذهن انسان.",
        "release_date": "2010-07-16",
        "poster_url": "https://www.example.com/inception-poster.jpg",  # لینک فرضی
        "download_links": {
            "480p": "https://pl.ortatv.fun/Inception-480p.mp4",
            "720p": "https://pl.ortatv.fun/Inception-720p.mp4",
            "1080p": "https://pl.ortatv.fun/Inception-1080p.mp4"
        }
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_name = context.args[0] if context.args else None
    if not movie_name or movie_name not in MOVIE_DATA:
        await update.message.reply_text("❌ فیلم مورد نظر پیدا نشد. لطفاً نام فیلم را وارد کنید.")
        return

    movie = MOVIE_DATA[movie_name]
    title = movie["title"]
    description = movie["description"]
    release_date = movie["release_date"]
    poster_url = movie["poster_url"]
    download_links = movie["download_links"]

    # ساخت پیام
    links_message = "\n".join([f"📥 [کیفیت {quality}]({url})" for quality, url in download_links.items()])
    message = f"""
🎬 {title}

📖 توضیحات: {description}
🗓 تاریخ انتشار: {release_date}

⬇️ لینک‌های دانلود:
{links_message}
    """

    # ارسال پیام و پوستر فیلم
    await update.message.reply_photo(poster_url, caption=message, parse_mode="Markdown", disable_web_page_preview=True)

if __name__ == "__main__":
    # توکن ربات را از متغیر محیطی دریافت کنید
    token = os.getenv("BOT_TOKEN")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
