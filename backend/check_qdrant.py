from qdrant_client import QdrantClient

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "research_papers"

client = QdrantClient(url=QDRANT_URL)

points, next_page = client.scroll(
    collection_name=COLLECTION_NAME,
    limit=1000,
    with_payload=True,
    with_vectors=False
)

print("\n" + "=" * 60)
print("CURRENT QDRANT PAPERS")
print("=" * 60)

papers = {}

for point in points:
    payload = point.payload or {}

    paper_id = payload.get("paper_id", "UNKNOWN")
    title = payload.get("title", "UNKNOWN")
    year = payload.get("year", "UNKNOWN")

    papers[paper_id] = {
        "title": title,
        "year": year
    }

print(f"\nTotal vectors: {len(points)}")
print(f"Unique papers: {len(papers)}")

print("\nPapers stored:\n")

for i, (paper_id, info) in enumerate(papers.items(), start=1):
    print(f"{i}. {info['title']}")
    print(f"   Year: {info['year']}")
    print(f"   Paper ID: {paper_id}")
    print()

print("=" * 60)