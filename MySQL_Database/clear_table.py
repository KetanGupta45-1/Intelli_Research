def clear_articles_table(connection):
    """Truncate (clear) the articles table."""
    if connection is None:
        print("⚠️ No active connection. Please connect first.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE articles")
        connection.commit()
        cursor.close()
        print("🧹\n Cleared all existing data from 'articles' table.")
    except Exception as e:
        print(f"❌ Error clearing table: {e}")