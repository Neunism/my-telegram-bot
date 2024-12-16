from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import os
import requests

# دریافت API Key از متغیر محیطی
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# تابع استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تعریف دکمه‌ها
    keyboard = [
        [
            InlineKeyboardButton("🎥 فیلم‌های داغ", callback_data="hot_movies"),
            InlineKeyboardButton("🌟 پرفروش‌ترین‌ها", callback_data="top_sellers")
        ],
        [
            InlineKeyboardButton("⚡ ارتقاء پکیج", callback_data="upgrade_package"),
            InlineKeyboardButton("🎬 فیلم‌های جدید", callback_data="new_movies")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # ارسال پیام خوش‌آمدگویی همراه با دکمه‌ها
    await update.message.reply_text(
        "سلام! خوش آمدید.\nیکی از گزینه‌های زیر را انتخاب کنید یا نام فیلم را برای جستجو ارسال کنید:",
        reply_markup=reply_markup
    )

# مدیریت کلیک روی دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # واکنش به هر دکمه بر اساس callback_data
    if query.data == "hot_movies":
        await query.edit_message_text("🔥 فیلم‌های داغ در حال بارگذاری هستند...")
    elif query.data == "top_sellers":
        await query.edit_message_text("🌟 لیست پرفروش‌ترین فیلم‌ها در حال آماده‌سازی است...")
    elif query.data == "upgrade_package":
        await query.edit_message_text("⚡ لطفاً جهت ارتقاء پکیج خود به وب‌سایت ما مراجعه کنید.")
    elif query.data == "new_movies":
        await query.edit_message_text("🎬 فیلم‌های جدید در حال بارگذاری هستند...")

# جستجوی فیلم
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

# اجرای ربات
if __name__ == "__main__":
    # دریافت توکن ربات از متغیر محیطی
    token = os.getenv("BOT_TOKEN")

    # ایجاد اپلیکیشن ربات
    app = ApplicationBuilder().token(token).build()

    # ثبت هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))

    # اجرای ربات
    app.run_polling()
