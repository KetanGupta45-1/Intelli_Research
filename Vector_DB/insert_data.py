# insert_data.py

def insert_papers(collection, model, papers):
    titles = [paper.get("title", "N/A") for paper in papers]
    ids = [str(i) for i in range(1, len(titles) + 1)]
    embeddings = model.encode(titles).tolist()
    print('\n Inserting Papers in Vector DB')

    collection.add(
        ids=ids,
        documents=titles,
        embeddings=embeddings,
        metadatas=papers
    )
