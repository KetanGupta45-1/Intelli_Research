import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from MySQL_Database.get_connection import get_connection
from MySQL_Database.create_table import create_table
from MySQL_Database.insert_to_table import insert_paper
from MySQL_Database.clear_table import clear_articles_table
from MySQL_Database.collect_papers import collect_papers


class MySQLMain:
    def __init__(self):
        self.connection = None
        print("✅ MySQLMain initialized.")

    def connect(self):
        """Establish a database connection."""
        self.connection = get_connection()
        if self.connection:
            print("✅ Connected successfully to MySQL database.")
        else:
            print("❌ Failed to connect to MySQL database.")

    def create_articles_table(self):
        """Create 'articles' table if it doesn't exist."""
        create_table()

    def clear_table(self):
        """Clear data from 'articles' table."""
        clear_articles_table(self.connection)

    def collect_papers(self, topic, max_papers=20, save_to_file=False):
        """Collect papers using crawler logic."""
        return collect_papers(topic, max_papers, save_to_file)

    def insert_papers(self, papers):
        """Insert multiple papers into MySQL database."""
        if self.connection is None:
            print("⚠️ No active connection. Please connect first.")
            return
        if not papers:
            print("⚠️ No papers to insert.")
            return

        for paper in papers:
            insert_paper(self.connection, paper)
        print(f"✅ Inserted {len(papers)} papers into 'articles' table.")

    def close_connection(self):
        """Close the active MySQL connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            print("🔒 Database connection closed.")
        else:
            print("⚠️ No connection to close.")