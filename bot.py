from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import sqlite3

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! نام فیلم مورد نظر را ارسال کنید.")

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    # جستجو برای فیلم در پایگاه داده
    cursor.execute("SELECT * FROM movies WHERE title LIKE ?", ('%' + query + '%',))
    movie = cursor.fetchone()

    conn.close()

    if not movie:
        await update.message.reply_text("❌ فیلم پیدا نشد.")
        return

    title, description, release_date, quality_480p, quality_720p, quality_1080p = movie[1:]
    links = ""
    if quality_480p: links += f"📥 [480p]({quality_480p})\n"
    if quality_720p: links += f"📥 [720p]({quality_720p})\n"
    if quality_1080p: links += f"📥 [1080p]({quality_1080p})\n"

    message = (
        f"🎬 {title}\n\n"
        f"📖 توضیحات: {description}\n"
        f"🗓 تاریخ انتشار: {release_date}\n\n"
        f"⬇️ لینک‌های دانلود:\n{links}"
    )
    await update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)

# اجرای ربات
if __name__ == '__main__':
    from telegram.ext import ApplicationBuilder

    # دریافت توکن از متغیر محیطی
    import os
    token = os.getenv("BOT_TOKEN")

    # ایجاد اپلیکیشن با توکن
    app = ApplicationBuilder().token(token).build()

    # راه‌اندازی ربات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))

    app.run_polling()
