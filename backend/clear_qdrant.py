
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
collection_name = "research_papers"

if client.collection_exists(collection_name):
    client.delete_collection(collection_name)
    print(f"Collection '{collection_name}' deleted.")
else:
    print(f"Collection '{collection_name}' does not exist.")

print("Qdrant cleanup completed.")