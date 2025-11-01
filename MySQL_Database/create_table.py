from MySQL_Database.get_connection import get_connection
from mysql.connector import Error

def create_table():
    db = get_connection()
    if db is None:
        print("⚠️ Could not establish database connection. Aborting table creation.")
        return

    try:
        cursor = db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title TEXT,
            authors TEXT,
            pub_date VARCHAR(100),
            abstract TEXT,
            paper_link TEXT
        )
        """)
        db.commit()
        print("✅\n  Table 'articles' is ready.")
    except Error as e:
        print(f"❌ Error while creating table: {e}")
    finally:
        cursor.close()
        db.close()