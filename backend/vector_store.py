import json
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "research_papers"
QDRANT_URL = "http://localhost:6333"


def get_qdrant_client():
    """
    Create a connection to the Qdrant Docker server.
    """
    return QdrantClient(url=QDRANT_URL)


def reset_vector_store():
    """
    Delete the existing research collection.

    This is useful when starting a fresh research corpus.
    """

    client = get_qdrant_client()

    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)
        print("Existing Qdrant collection deleted.")
    else:
        print("Qdrant collection did not exist.")

    print("Qdrant collection reset successfully.")


def load_chunks(input_file):
    """
    Load chunk data from a JSON file.
    """

    with open(input_file, "r", encoding="utf-8") as file:
        return json.load(file)


def create_vector_store(chunks, embeddings):
    """
    Store chunk embeddings and metadata in Qdrant.
    """

    client = get_qdrant_client()

    vector_size = len(embeddings[0])

    # -------------------------------------
    # Create collection if it doesn't exist
    # -------------------------------------
    if not client.collection_exists(COLLECTION_NAME):

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

        print("Qdrant collection created.")

    # -------------------------------------
    # Prepare points
    # -------------------------------------
    points = []

    for chunk, embedding in zip(chunks, embeddings):

        # Deterministic unique ID
        #
        # Same paper + same chunk
        # always produces the same UUID.
        point_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_DNS,
                f"{chunk['paper_id']}_{chunk['chunk_id']}"
            )
        )

        points.append(
            PointStruct(
                id=point_id,
                vector=embedding.tolist(),
                payload={
                    "paper_id": chunk["paper_id"],
                    "title": chunk["title"],
                    "year": chunk["year"],
                    "doi": chunk["doi"],
                    "chunk_id": chunk["chunk_id"],
                    "section": chunk["section"],
                    "word_count": chunk["word_count"],
                    "text": chunk["text"]
                }
            )
        )

    # -------------------------------------
    # Store vectors
    # -------------------------------------
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print("Vectors stored successfully!")

    # -------------------------------------
    # Show collection information
    # -------------------------------------
    collection_info = client.get_collection(
        collection_name=COLLECTION_NAME
    )

    print(
        "Vectors in collection:",
        collection_info.points_count
    )

    return client


if __name__ == "__main__":

    print("\n========================================")
    print("        QDRANT COLLECTION RESET")
    print("========================================")

    reset_vector_store()

    print("\nQdrant is now ready for fresh ingestion.")