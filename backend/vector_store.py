import json
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "research_papers"


def load_chunks(input_file):
    with open(input_file, "r", encoding="utf-8") as file:
        return json.load(file)


def create_vector_store(chunks, embeddings):

    #client = QdrantClient(path="data/qdrant") for storing in the sqlite
    client= QdrantClient(
        url= 'http://localhost:6333'
    )

    vector_size = len(embeddings[0])

    # Create collection if it does not already exist
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

    points = []

    for index, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):

        points.append(
            PointStruct(
                id=index,
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

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print("Vectors stored successfully!")

    collection_info = client.get_collection(
        collection_name=COLLECTION_NAME
    )

    print(
        "Vectors in collection:",
        collection_info.points_count
    )

    return client


if __name__ == "__main__":

    chunks_file = "data/papers/chunks/test_paper_chunks.json"

    chunks = load_chunks(chunks_file)

    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    print("Total chunks:", len(chunks))
    print("Embedding dimension:", len(embeddings[0]))

    create_vector_store(
        chunks,
        embeddings
    )