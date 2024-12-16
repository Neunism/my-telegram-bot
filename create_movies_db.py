import sqlite3

# ایجاد فایل پایگاه داده و اتصال به آن
conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

# ایجاد جدول movies
cursor.execute('''
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    release_date TEXT,
    quality_480p TEXT,
    quality_720p TEXT,
    quality_1080p TEXT
)
''')

print("پایگاه داده و جدول movies با موفقیت ایجاد شدند.")

# ذخیره تغییرات و بستن اتصال
conn.commit()
conn.close()
