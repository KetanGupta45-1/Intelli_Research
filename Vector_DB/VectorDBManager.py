# vector_db_manager.py
from Vector_DB.init_connection import initialize_chroma
from Vector_DB.insert_data import insert_papers
from Vector_DB.query_data import search
from Vector_DB.clear_collection import clear

class VectorDBManager:
    def __init__(self, db_path="chroma_db", collection_name="article_embeddings"):
        self.client, self.collection, self.model = initialize_chroma(db_path, collection_name)
        print("✅ VectorDBManager initialized successfully.")

    def insert_papers(self, papers):
        """Insert papers into vector database"""
        insert_papers(self.collection, self.model, papers)
        print(f"✅ Inserted {len(papers)} embeddings into ChromaDB.")

    def search(self, query, top_k=5):
        """Search for similar papers"""
        results = search(self.collection, self.model, query, top_k)

        print(f"\n🔍 Search results for '{query}':")
        
        for i, title in enumerate(results["documents"][0]):
            score = results["distances"][0][i]
            print(f"  {i+1}. {title} (distance: {score:.4f})")
        return results

    def clear(self):
        """Clear the collection"""
        self.collection = clear(self.client, self.collection)
        print(f"🧹 Cleared all data in collection '{self.collection.name}'.")
