from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# Configuration
# --------------------------------------------------

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "research_papers"
QDRANT_URL = "http://localhost:6333"


# --------------------------------------------------
# Semantic Search
# --------------------------------------------------

def search_papers(query, top_k=3):
    """
    Convert the user's query into an embedding
    and retrieve the most relevant research chunks
    from Qdrant.
    """

    # Connect to Docker Qdrant
    client = QdrantClient(
        url=QDRANT_URL
    )

    # Load embedding model
    model = SentenceTransformer(
        MODEL_NAME
    )

    # Convert query into vector
    query_embedding = model.encode(
        query
    ).tolist()

    # Search Qdrant
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=top_k,
        with_payload=True
    ).points

    return results


# --------------------------------------------------
# Build Research Context
# --------------------------------------------------

def build_research_context(results):
    """
    Convert Qdrant search results into a structured
    research context.

    This context can later be passed to an LLM
    for research analysis and answer generation.
    """

    context = []

    for i, result in enumerate(
        results,
        start=1
    ):

        payload = result.payload

        source = {
            "source_number": i,
            "relevance_score": round(
                result.score,
                4
            ),
            "paper_id": payload.get(
                "paper_id"
            ),
            "title": payload.get(
                "title"
            ),
            "year": payload.get(
                "year"
            ),
            "doi": payload.get(
                "doi"
            ),
            "section": payload.get(
                "section"
            ),
            "chunk_id": payload.get(
                "chunk_id"
            ),
            "text": payload.get(
                "text"
            )
        }

        context.append(
            source
        )

    return context


# --------------------------------------------------
# Display Search Results
# --------------------------------------------------

def display_results(results):
    """
    Display the retrieved research sources
    in a readable format.
    """

    print(
        "\n===== SEMANTIC SEARCH RESULTS ====="
    )

    for i, result in enumerate(
        results,
        start=1
    ):

        payload = result.payload

        print(
            f"\n{'=' * 60}"
        )

        print(
            f"Result {i}"
        )

        print(
            "Relevance Score:",
            round(
                result.score,
                4
            )
        )

        print(
            "Paper ID:",
            payload.get(
                "paper_id"
            )
        )

        print(
            "Title:",
            payload.get(
                "title"
            )
        )

        print(
            "Year:",
            payload.get(
                "year"
            )
        )

        print(
            "DOI:",
            payload.get(
                "doi"
            )
        )

        print(
            "Section:",
            payload.get(
                "section"
            )
        )

        print(
            "Chunk ID:",
            payload.get(
                "chunk_id"
            )
        )

        print(
            "Word Count:",
            payload.get(
                "word_count"
            )
        )

        print(
            "\nEvidence:"
        )

        print(
            payload.get(
                "text",
                ""
            )[:1000]
        )

    print(
        f"\n{'=' * 60}"
    )


# --------------------------------------------------
# Display Research Context
# --------------------------------------------------

def display_research_context(context):
    """
    Display the structured research context
    that will later be given to the AI analysis layer.
    """

    print(
        "\n===== RESEARCH CONTEXT ====="
    )

    for source in context:

        print(
            f"\n{'-' * 60}"
        )

        print(
            f"SOURCE {source['source_number']}"
        )

        print(
            "Title:",
            source["title"]
        )

        print(
            "Year:",
            source["year"]
        )

        print(
            "Section:",
            source["section"]
        )

        print(
            "Relevance:",
            source["relevance_score"]
        )

        print(
            "Evidence:",
            source["text"][:500]
        )

    print(
        f"\n{'-' * 60}"
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    # Research question
    query = (
        "How can generative AI "
        "support learning and education?"
    )

    # ----------------------------------------------
    # Step 1: Retrieve relevant chunks
    # ----------------------------------------------

    results = search_papers(
        query,
        top_k=3
    )

    # ----------------------------------------------
    # Step 2: Display raw search results
    # ----------------------------------------------

    display_results(
        results
    )

    # ----------------------------------------------
    # Step 3: Build structured research context
    # ----------------------------------------------

    research_context = build_research_context(
        results
    )

    # ----------------------------------------------
    # Step 4: Display research context
    # ----------------------------------------------

    display_research_context(
        research_context
    )