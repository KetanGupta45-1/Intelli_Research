from mysql.connector import Error
def insert_paper(db, paper):
    try:
        cursor = db.cursor()
        query = """
            INSERT INTO articles (title, authors, pub_date, abstract, paper_link)
            VALUES (%s, %s, %s, %s, %s)
        """
        data = (
            paper.get("title", "N/A"),
            paper.get("authors", "N/A"),
            paper.get("date", "N/A"),
            paper.get("abstract", "N/A"),
            paper.get("link", "N/A")
        )
        cursor.execute(query, data)
        db.commit()

        print('\n Papers Inserted')
    except Error as e:
        print(f"❌ Error inserting paper: {e}")
    finally:
        cursor.close()