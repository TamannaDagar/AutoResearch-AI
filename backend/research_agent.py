from semantic_search import (
    search_papers,
    build_research_context
)

from llm_client import generate_answer


def build_analysis_prompt(research_context):

    question = research_context["question"]

    papers = research_context["papers"]

    evidence = research_context["evidence"]

    prompt = f"""
You are a research analysis assistant.

Your task is to answer the research question
using ONLY the research evidence provided below.

IMPORTANT RULES:

1. Use only the provided research evidence.
2. Do not invent facts or sources.
3. Do not introduce outside knowledge.
4. Clearly distinguish evidence from interpretation.
5. When making an important claim, identify the supporting source number.
6. If the evidence is insufficient, explicitly say so.
7. Prefer direct evidence from the retrieved research chunks.
8. Do not treat relevance scores as evidence.
9. Do not make claims about a paper that are not supported
   by the provided evidence.

RESEARCH QUESTION:

{question}


RESEARCH PAPERS:

"""

    for index, paper in enumerate(
        papers,
        start=1
    ):

        prompt += f"""
PAPER {index}

Title:
{paper["title"]}

Year:
{paper["year"]}

DOI:
{paper["doi"]}

Paper ID:
{paper["paper_id"]}

----------------------------------------
"""

    prompt += """

RETRIEVED RESEARCH EVIDENCE:

"""

    for source in evidence:

        prompt += f"""
SOURCE {source["source_number"]}

Paper:
{source["title"]}

Year:
{source["year"]}

Section:
{source["section"]}

Chunk ID:
{source["chunk_id"]}

Relevance Score:
{source["relevance_score"]}

Evidence:
{source["text"]}

----------------------------------------
"""

    prompt += """

ANALYSIS TASK:

Based ONLY on the retrieved evidence:

1. Identify findings that are directly relevant to the question.
2. Explain what the evidence supports.
3. Identify important limitations or uncertainties.
4. Distinguish direct evidence from interpretation.
5. Provide a concise research-oriented synthesis.
6. Cite the source number for important claims.

If the retrieved evidence does not provide enough information
to answer part of the question, explicitly state that the
available evidence is insufficient.

Do not introduce outside information.
"""

    return prompt


def research_agent(
    question,
    top_k=5
):

    # -------------------------------------
    # Step 1: Semantic search
    # -------------------------------------

    results = search_papers(
        question,
        top_k=top_k
    )

    # -------------------------------------
    # Step 2: Build research context
    # -------------------------------------

    research_context = build_research_context(
        question,
        results
    )

    # -------------------------------------
    # Step 3: Build analysis prompt
    # -------------------------------------

    analysis_prompt = build_analysis_prompt(
        research_context
    )

    # -------------------------------------
    # Step 4: Generate answer
    # -------------------------------------

    answer = generate_answer(
        analysis_prompt
    )

    # -------------------------------------
    # Step 5: Return complete result
    # -------------------------------------

    return {

        "question": question,

        "answer": answer,

        "research_context": research_context,

        "sources": research_context[
            "evidence"
        ],

        "source_count": research_context[
            "evidence_count"
        ]
    }


# -----------------------------------------
# Test
# -----------------------------------------

if __name__ == "__main__":

    question = (
        "How can generative AI support "
        "learning and education?"
    )

    result = research_agent(
        question,
        top_k=3
    )

    print(
        "\n========================================"
    )

    print(
        "         RESEARCH AGENT"
    )

    print(
        "========================================"
    )

    print(
        "\nResearch Question:"
    )

    print(
        result["question"]
    )

    print(
        "\nPapers Retrieved:"
    )

    print(
        result["research_context"][
            "paper_count"
        ]
    )

    print(
        "\nEvidence Retrieved:"
    )

    print(
        result["research_context"][
            "evidence_count"
        ]
    )

    print(
        "\n========================================"
    )

    print(
        "       GEMINI RESEARCH ANALYSIS"
    )

    print(
        "========================================"
    )

    print(
        result["answer"]
    )

    print(
        "\n========================================"
    )

    print(
        "           SOURCES USED"
    )

    print(
        "========================================"
    )

    for source in result["sources"]:

        print(
            f"\n[{source['source_number']}] "
            f"{source['title']} "
            f"({source['year']})"
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
        "\n========================================"
    )