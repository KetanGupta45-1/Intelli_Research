def clear(client, collection):
    name = collection.name
    client.delete_collection(name)
    print(f"🧹 Deleted existing collection '{name}'.")
    new_collection = client.get_or_create_collection(name=name)
    print(f"✅ Recreated empty collection '{name}'.")
    return new_collection