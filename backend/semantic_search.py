from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "research_papers"
QDRANT_URL = "http://localhost:6333"


def search_papers(
    query,
    top_k=5,
    allowed_sections=None,
    one_result_per_paper=False
):
    """
    Search the Qdrant research-paper collection.

    Parameters:
        query:
            Research question or search query.

        top_k:
            Number of evidence chunks to return.

        allowed_sections:
            Optional list of sections to search.
            Example:
                ["LIMITATIONS", "DISCUSSION", "CONCLUSION"]

        one_result_per_paper:
            If True, return at most one result from each paper.
            Useful for paper-level comparison.

            If False, multiple useful chunks from the same paper
            can be returned.
            Useful for evidence-based analysis.
    """

    client = QdrantClient(
        url=QDRANT_URL
    )

    model = SentenceTransformer(
        MODEL_NAME
    )

    query_embedding = model.encode(
        query
    ).tolist()

    # Retrieve more candidates than needed.
    # This gives section filtering and paper diversity
    # enough candidates to work with.
    candidate_limit = max(top_k * 10, 20)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=candidate_limit,
        with_payload=True
    ).points

    # Normalize allowed section names once.
    normalized_allowed_sections = None

    if allowed_sections:

        normalized_allowed_sections = {
            section.strip().upper()
            for section in allowed_sections
        }

    selected_results = []
    seen_papers = set()

    for result in results:

        payload = result.payload

        # ----------------------------------------
        # SECTION FILTER
        # ----------------------------------------

        section = payload.get(
            "section",
            ""
        ).strip().upper()

        if normalized_allowed_sections:

            if section not in normalized_allowed_sections:
                continue

        # ----------------------------------------
        # PAPER DIVERSITY
        # ----------------------------------------

        paper_id = payload.get(
            "paper_id"
        )

        if one_result_per_paper:

            if paper_id in seen_papers:
                continue

            seen_papers.add(paper_id)

        # ----------------------------------------
        # ADD RESULT
        # ----------------------------------------

        selected_results.append(
            result
        )

        if len(selected_results) >= top_k:
            break

    return selected_results


def build_research_context(
    question,
    results
):
    """
    Convert raw Qdrant search results into a
    reusable research context.

    This structure can be shared by:

        Research Agent
        Compare Agent
        Gap Agent
        Evidence Agent
        Synthesis Agent
        Literature Review Agent
    """

    evidence = []

    papers = {}

    for index, result in enumerate(
        results,
        start=1
    ):

        payload = result.payload

        paper_id = payload.get(
            "paper_id"
        )

        # ----------------------------------------
        # EVIDENCE OBJECT
        # ----------------------------------------

        evidence_item = {

            "source_number": index,

            "relevance_score": round(
                result.score,
                4
            ),

            "paper_id": paper_id,

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

            "word_count": payload.get(
                "word_count"
            ),

            "text": payload.get(
                "text"
            )
        }

        evidence.append(
            evidence_item
        )

        # ----------------------------------------
        # UNIQUE PAPER
        # ----------------------------------------

        if paper_id not in papers:

            papers[paper_id] = {

                "paper_id": paper_id,

                "title": payload.get(
                    "title"
                ),

                "year": payload.get(
                    "year"
                ),

                "doi": payload.get(
                    "doi"
                )
            }

    # ----------------------------------------
    # FINAL RESEARCH CONTEXT
    # ----------------------------------------

    return {

        "question": question,

        "papers": list(
            papers.values()
        ),

        "evidence": evidence,

        "evidence_count": len(
            evidence
        ),

        "paper_count": len(
            papers
        )
    }


def display_research_context(
    research_context
):
    """
    Display the structured research context
    in the terminal.
    """

    print(
        "\n===== RESEARCH CONTEXT ====="
    )

    print(
        "\nQuestion:",
        research_context["question"]
    )

    print(
        "Papers:",
        research_context["paper_count"]
    )

    print(
        "Evidence items:",
        research_context["evidence_count"]
    )

    for source in research_context[
        "evidence"
    ]:

        print(
            f"\n{'-' * 60}"
        )

        print(
            "SOURCE:",
            source["source_number"]
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
            "Chunk:",
            source["chunk_id"]
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


def display_results(
    results
):
    """
    Display raw semantic-search results.
    """

    print(
        "\n===== SEMANTIC SEARCH RESULTS ====="
    )

    for index, result in enumerate(
        results,
        start=1
    ):

        payload = result.payload

        print(
            f"\n{'=' * 60}"
        )

        print(
            f"Result {index}"
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


if __name__ == "__main__":

    query = (
        "How can generative AI support "
        "learning and education?"
    )

    # Normal evidence search.
    #
    # Multiple chunks from the same paper
    # are allowed.
    results = search_papers(
        query,
        top_k=5
    )

    display_results(
        results
    )

    research_context = build_research_context(
        query,
        results
    )

    display_research_context(
        research_context
    )