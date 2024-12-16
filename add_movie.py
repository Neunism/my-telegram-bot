import sqlite3

def add_movie(title, description, release_date, quality_480p, quality_720p, quality_1080p):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            release_date TEXT,
            quality_480p TEXT,
            quality_720p TEXT,
            quality_1080p TEXT
        )
    ''')

    cursor.execute('''
        INSERT INTO movies (title, description, release_date, quality_480p, quality_720p, quality_1080p)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, description, release_date, quality_480p, quality_720p, quality_1080p))

    conn.commit()
    conn.close()
    print(f"✅ فیلم '{title}' با موفقیت اضافه شد.")

if __name__ == "__main__":
    # نمونه فیلم برای اضافه کردن
    add_movie(
        title="Inception",
        description="یک فیلم علمی تخیلی به کارگردانی کریستوفر نولان.",
        release_date="2010-07-16",
        quality_480p="https://pl.ortatv.fun/inception-480p.mp4",
        quality_720p="https://pl.ortatv.fun/inception-720p.mp4",
        quality_1080p="https://pl.ortatv.fun/inception-1080p.mp4"
    )
