import sqlite3

# اتصال به پایگاه داده
conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

# تابع برای اضافه کردن فیلم
def add_movie(title, description, release_date, quality_480p, quality_720p, quality_1080p):
    cursor.execute('''
        INSERT INTO movies (title, description, release_date, quality_480p, quality_720p, quality_1080p)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, description, release_date, quality_480p, quality_720p, quality_1080p))
    conn.commit()

# مثال: اضافه کردن یک فیلم جدید
add_movie(
    "Inception",
    "فیلم Inception یک فیلم علمی تخیلی است که توسط کریستوفر نولان کارگردانی شده است.",
    "2010-07-16",
    "https://link.to/480p",
    "https://link.to/720p",
    "https://link.to/1080p"
)

print("فیلم با موفقیت اضافه شد!")

# بستن اتصال به پایگاه داده
conn.close()
