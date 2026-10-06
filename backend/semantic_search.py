
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
)
from sentence_transformers import SentenceTransformer


# ==========================================
# CONFIGURATION
# ==========================================

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "research_papers"
QDRANT_URL = "http://localhost:6333"


# Load the embedding model once and reuse it.
print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)
print("Embedding model loaded successfully.")


# ==========================================
# SEMANTIC SEARCH
# ==========================================

def search_papers(
    query,
    top_k=5,
    allowed_sections=None,
    one_result_per_paper=False,
    paper_ids=None,
):
    """
    Search the Qdrant research-paper collection.

    Parameters:
        query:
            Research question or search query.

        top_k:
            Maximum number of evidence chunks to return.

        allowed_sections:
            Optional list of sections to search.
            Example:
                ["LIMITATIONS", "DISCUSSION", "CONCLUSION"]

        one_result_per_paper:
            If True, return at most one result per paper.
            Useful for paper-level comparison.

            If False, multiple chunks from the same paper
            can be returned.
            Useful for evidence-based analysis.

    Returns:
        List of Qdrant search results.
    """

    # --------------------------------------
    # 1. Validate input
    # --------------------------------------

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    # --------------------------------------
    # 2. Connect to Qdrant
    # --------------------------------------

    client = QdrantClient(
        url=QDRANT_URL
    )

    if not client.collection_exists(COLLECTION_NAME):
        raise ValueError(
            f"Qdrant collection '{COLLECTION_NAME}' does not exist."
        )

    # --------------------------------------
    # 3. Generate query embedding
    # --------------------------------------

    query_embedding = model.encode(
        query,
        convert_to_numpy=True,
    ).tolist()

    # --------------------------------------
    # 4. Retrieve candidate chunks
    # --------------------------------------

    candidate_limit = max(
        top_k * 10,
        20,
    )

        # --------------------------------------
    # 4.5 Build paper filter
    # --------------------------------------

    query_filter = None

    if paper_ids:
        query_filter = Filter(
            should=[
                FieldCondition(
                    key="paper_id",
                    match=MatchValue(value=paper_id),
                )
                for paper_id in paper_ids
            ]
        )

    results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_embedding,
    query_filter=query_filter,
    limit=candidate_limit,
    with_payload=True,
).points

    # --------------------------------------
    # 5. Normalize section filters
    # --------------------------------------

    normalized_allowed_sections = None

    if allowed_sections:
        normalized_allowed_sections = {
            section.strip().upper()
            for section in allowed_sections
        }

    # --------------------------------------
    # 6. Filter and select results
    # --------------------------------------

    selected_results = []
    seen_papers = set()

    for result in results:

        payload = result.payload or {}

        # Section filtering
        section = payload.get(
            "section",
            "",
        ).strip().upper()

        if normalized_allowed_sections is not None:
            if section not in normalized_allowed_sections:
                continue

        # Paper diversity
        paper_id = payload.get("paper_id")

        if one_result_per_paper:
            if paper_id in seen_papers:
                continue

            seen_papers.add(paper_id)

        selected_results.append(result)

        if len(selected_results) >= top_k:
            break

    # --------------------------------------
    # 7. Display retrieval statistics
    # --------------------------------------

    print("\n===== SEARCH STATISTICS =====")
    print("Query:", query)
    print("Candidates retrieved:", len(results))
    print("Results selected:", len(selected_results))
    print("Requested results:", top_k)

    if normalized_allowed_sections:
        print(
            "Allowed sections:",
            sorted(normalized_allowed_sections),
        )

    if one_result_per_paper:
        print("Paper diversity: Enabled")
    else:
        print("Paper diversity: Disabled")

    return selected_results


# ==========================================
# BUILD RESEARCH CONTEXT
# ==========================================

def build_research_context(
    question,
    results,
):
    """
    Convert Qdrant search results into a
    structured research context.

    This context can be shared with:
        Research Agent
        Compare Agent
        Gap Agent
        Evidence Agent
        Trend Agent
        Synthesis Agent
        Literature Review Agent
    """

    evidence = []
    papers = {}

    for index, result in enumerate(
        results,
        start=1,
    ):

        payload = result.payload or {}

        paper_id = payload.get("paper_id")

        # --------------------------------------
        # Evidence object
        # --------------------------------------

        evidence_item = {
            "source_number": index,
            "relevance_score": round(
                float(result.score),
                4,
            ),
            "paper_id": paper_id,
            "title": payload.get("title"),
            "year": payload.get("year"),
            "doi": payload.get("doi"),
            "section": payload.get("section"),
            "chunk_id": payload.get("chunk_id"),
            "word_count": payload.get("word_count"),
            "text": payload.get("text"),
        }

        evidence.append(evidence_item)

        # --------------------------------------
        # Unique paper information
        # --------------------------------------

        if paper_id not in papers:
            papers[paper_id] = {
                "paper_id": paper_id,
                "title": payload.get("title"),
                "year": payload.get("year"),
                "doi": payload.get("doi"),
            }

    # --------------------------------------
    # Final research context
    # --------------------------------------

    return {
        "question": question,
        "papers": list(papers.values()),
        "evidence": evidence,
        "evidence_count": len(evidence),
        "paper_count": len(papers),
    }


# ==========================================
# DISPLAY RESEARCH CONTEXT
# ==========================================

def display_research_context(
    research_context,
):
    """
    Display structured research context
    in the terminal.
    """

    print("\n===== RESEARCH CONTEXT =====")

    print(
        "\nQuestion:",
        research_context["question"],
    )

    print(
        "Papers:",
        research_context["paper_count"],
    )

    print(
        "Evidence items:",
        research_context["evidence_count"],
    )

    for source in research_context["evidence"]:

        print("\n" + "-" * 60)

        print(
            "SOURCE:",
            source["source_number"],
        )

        print(
            "Title:",
            source["title"],
        )

        print(
            "Year:",
            source["year"],
        )

        print(
            "Section:",
            source["section"],
        )

        print(
            "Chunk:",
            source["chunk_id"],
        )

        print(
            "Relevance:",
            source["relevance_score"],
        )

        print("\nEvidence:")

        print(
            (source["text"] or "")[:500]
        )

    print("\n" + "-" * 60)


# ==========================================
# DISPLAY RAW SEARCH RESULTS
# ==========================================

def display_results(
    results,
):
    """
    Display raw semantic-search results.
    """

    print("\n===== SEMANTIC SEARCH RESULTS =====")

    if not results:
        print("No matching evidence was found.")
        return

    for index, result in enumerate(
        results,
        start=1,
    ):

        payload = result.payload or {}

        print("\n" + "=" * 60)

        print(
            f"Result {index}"
        )

        print(
            "Relevance Score:",
            round(float(result.score), 4),
        )

        print(
            "Paper ID:",
            payload.get("paper_id"),
        )

        print(
            "Title:",
            payload.get("title"),
        )

        print(
            "Year:",
            payload.get("year"),
        )

        print(
            "DOI:",
            payload.get("doi"),
        )

        print(
            "Section:",
            payload.get("section"),
        )

        print(
            "Chunk ID:",
            payload.get("chunk_id"),
        )

        print(
            "Word Count:",
            payload.get("word_count"),
        )

        print("\nEvidence:")

        print(
            (payload.get("text") or "")[:1000]
        )

    print("\n" + "=" * 60)


# ==========================================
# MAIN TEST
# ==========================================

if __name__ == "__main__":

    query = (
        "What benefits and challenges of generative AI in higher education are reported by students and researchers?"
    )

    # Search for up to five relevant chunks.
    # Multiple chunks from one paper are allowed.
    results = search_papers(
        query=query,
        top_k=5,
        one_result_per_paper=True,
    )

    # Display individual results.
    display_results(results)

    # Build structured context for the agents.
    research_context = build_research_context(
        query,
        results,
    )

    # Display the structured research context.
    display_research_context(
        research_context,
    )