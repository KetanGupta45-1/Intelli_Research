# init_connection.py
import chromadb
from sentence_transformers import SentenceTransformer

def initialize_chroma(db_path, collection_name):
    client = chromadb.PersistentClient(path=db_path)
    print("✅ Connected to ChromaDB.")

    collection = client.get_or_create_collection(name=collection_name)
    print(f"✅ Collection '{collection_name}' is ready.")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Embedding model loaded.")

    return client, collection, model
