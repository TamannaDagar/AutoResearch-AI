from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "research_papers"


def search_papers(query, top_k=3):

    # Connect to Qdrant running in Docker
    client = QdrantClient(
        url="http://localhost:6333"
    )

    # Load the same embedding model used when storing vectors
    model = SentenceTransformer(MODEL_NAME)

    # Convert user's question into an embedding
    query_embedding = model.encode(query).tolist()

    # Search Qdrant
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=top_k,
        with_payload=True
    ).points

    return results


if __name__ == "__main__":

    query = "How can generative AI support learning and education?"

    results = search_papers(query, top_k=3)

    print("\n===== SEMANTIC SEARCH RESULTS =====")

    for i, result in enumerate(results, start=1):

        print(f"\nResult {i}")
        print("Score:", result.score)
        print("Chunk ID:", result.payload["chunk_id"])
        print("Text:")
        print(result.payload["text"][:1000])