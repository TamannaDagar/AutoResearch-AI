
import json
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "research_papers"
QDRANT_URL = "http://localhost:6333"
EXPECTED_VECTOR_SIZE = 384


def get_qdrant_client():
    """Connect to the Qdrant server."""
    return QdrantClient(url=QDRANT_URL)


def reset_vector_store():
    """
    Delete the entire research collection.

    Use only when intentionally starting a fresh corpus.
    """
    client = get_qdrant_client()

    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)
        print("Existing Qdrant collection deleted.")
    else:
        print("Qdrant collection did not exist.")

    print("Qdrant collection reset successfully.")


def load_chunks(input_file):
    """Load chunk data from a JSON file."""
    with open(input_file, "r", encoding="utf-8") as file:
        return json.load(file)


def ensure_collection(client, vector_size):
    """Create the collection or validate its vector configuration."""
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )
        print("Qdrant collection created.")
        return

    info = client.get_collection(COLLECTION_NAME)
    existing_config = info.config.params.vectors

    # This project uses a single unnamed vector per point.
    if existing_config.size != vector_size:
        raise ValueError(
            f"Collection vector size is {existing_config.size}, "
            f"but incoming embeddings have size {vector_size}. "
            "Reset or migrate the collection before inserting."
        )


def delete_paper_vectors(client, paper_id):
    """Delete all stored chunks belonging to one paper."""
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="paper_id",
                    match=MatchValue(value=paper_id),
                )
            ]
        ),
        wait=True,
    )
    print(f"Deleted existing vectors for paper: {paper_id}")


def create_vector_store(chunks, embeddings, replace_paper=False):
    """
    Store embeddings and chunk metadata in Qdrant.

    replace_paper=True removes existing vectors for each paper
    represented in the incoming chunks before inserting new ones.
    """
    if not chunks:
        raise ValueError("No chunks provided.")

    if len(chunks) != len(embeddings):
        raise ValueError(
            f"Chunk count ({len(chunks)}) does not match "
            f"embedding count ({len(embeddings)})."
        )

    vector_size = len(embeddings[0])

    if vector_size != EXPECTED_VECTOR_SIZE:
        raise ValueError(
            f"Expected {EXPECTED_VECTOR_SIZE}-dimensional embeddings, "
            f"received {vector_size}."
        )

    if any(len(vector) != vector_size for vector in embeddings):
        raise ValueError("Embedding dimensions are inconsistent.")

    client = get_qdrant_client()
    ensure_collection(client, vector_size)

    if replace_paper:
        paper_ids = {chunk["paper_id"] for chunk in chunks}
        for paper_id in paper_ids:
            delete_paper_vectors(client, paper_id)

    points = []

    for chunk, embedding in zip(chunks, embeddings):
        point_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_DNS,
                f"{chunk['paper_id']}_{chunk['chunk_id']}",
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
                    "text": chunk["text"],
                },
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
        wait=True,
    )

    print(f"Stored {len(points)} vectors successfully!")

    collection_info = client.get_collection(COLLECTION_NAME)
    print("Vectors in collection:", collection_info.points_count)

    return client


if __name__ == "__main__":
    print("\n========================================")
    print("        QDRANT COLLECTION RESET")
    print("========================================")

    reset_vector_store()
    print("\nQdrant is ready for fresh ingestion.")