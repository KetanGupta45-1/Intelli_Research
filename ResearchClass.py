# ResearchOrchestrator.py
from Crawler_Logic.Crawler import Crawler
from MySQL_Database.create_table import create_table
from MySQL_Database.get_connection import get_connection
from MySQL_Database.insert_to_table import insert_paper
from Vector_DB.VectorDBManager import VectorDBManager

class ResearchOrchestrator:
    def __init__(self, topic, max_papers=20, save_to_file=False,
                 chroma_db_path="chroma_db", collection_name="article_embeddings"):
        self.topic = topic
        self.max_papers = max_papers
        self.save_to_file = save_to_file

        self.crawler = Crawler(topic, max_papers, save_to_file)
        self.db_connection = None
        self.vector_db = VectorDBManager(db_path=chroma_db_path, collection_name=collection_name)

    def crawl_papers(self):
        print(f"\n🚀 Starting full crawl for topic: '{self.topic}'")
        self.papers = self.crawler.run_all()
        print(f"\n📦 Total papers collected: {len(self.papers)}")
        return self.papers

    def push_to_mysql(self):
        if not hasattr(self, "papers") or not self.papers:
            print("⚠️ No papers to push. Please run crawl_papers() first.")
            return

        create_table()
        self.db_connection = get_connection()
        if self.db_connection is None:
            print("❌ Database connection failed. Aborting push.")
            return

        cursor = self.db_connection.cursor()
        cursor.execute("TRUNCATE TABLE articles")
        self.db_connection.commit()
        cursor.close()
        print("🧹 Cleared old MySQL data.")

        for paper in self.papers:
            insert_paper(self.db_connection, paper)
        print(f"✅ Inserted {len(self.papers)} papers into MySQL.")

    def push_to_vector_db(self):
        if not hasattr(self, "papers") or not self.papers:
            print("⚠️ No papers to insert. Please run crawl_papers() first.")
            return

        self.vector_db.insert_papers(self.papers)

    def search_vector_db(self, query, top_k=5):
        self.vector_db.search(query, top_k)

    def clear_vector_db(self):
        self.vector_db.clear()

    # New unified function
    def run_pipeline(self, search_query=None, top_k=5, clear_before_push=False):
        if clear_before_push:
            self.clear_vector_db()

        print("Crawling Papers : ")
        print('\n')
        self.crawl_papers()
        
        print('Push to MySQL')
        print('\n')
        self.push_to_mysql()

        print('Push to Vector Database')
        print('\n')
        self.push_to_vector_db()

        if search_query:
            self.search_vector_db(search_query, top_k)
