def search(collection, model, query, top_k):
    query_emb = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_emb,
        n_results=top_k
    )
    return results
