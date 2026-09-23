from semantic_search import (
    search_papers,
    build_research_context
)

from llm_client import generate_answer


def build_gap_prompt(research_context):

    question = research_context["question"]
    papers = research_context["papers"]
    evidence = research_context["evidence"]

    prompt = f"""
You are a research gap analysis assistant.

Your task is to identify research gaps using ONLY
the research evidence provided below.

IMPORTANT RULES:

1. Use only the provided evidence.
2. Do not introduce outside knowledge.
3. Do not invent research gaps.
4. Do not assume that something is a gap merely because
   it is not mentioned in the retrieved evidence.
5. Prefer explicitly stated limitations and future research
   directions.
6. Clearly distinguish an explicitly stated research gap
   from an interpretation.
7. Cite the source number for every important gap.
8. If the evidence is insufficient, explicitly say so.
9. Do not treat relevance scores as evidence.

RESEARCH QUESTION:

{question}


RESEARCH PAPERS:

"""

    for index, paper in enumerate(papers, start=1):

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

Evidence:
{source["text"]}

----------------------------------------
"""

    prompt += """
GAP ANALYSIS TASK:

Based ONLY on the retrieved evidence:

1. Identify explicitly stated limitations.
2. Identify explicitly stated future research directions.
3. Identify unresolved research questions mentioned
   in the evidence.
4. Identify methodological limitations where supported.
5. Identify population, context, or dataset limitations
   where supported.
6. Identify potential research gaps only when the evidence
   provides sufficient support.
7. For every identified gap, cite the source number.
8. Clearly distinguish:
   - Explicitly stated gap
   - Evidence-based interpretation
   - Insufficient evidence

Do not invent gaps or introduce outside knowledge.

Provide a concise research-oriented gap analysis.
"""

    return prompt


def gap_agent(question, top_k=5):

    results = search_papers(
    question,
    top_k=top_k,
    allowed_sections=[
        "LIMITATIONS",
        "DISCUSSION",
        "CONCLUSION",
        "FUTURE WORK",
        "IMPLICATIONS",
        "RESULTS"
    ]
)
    research_context = build_research_context(
        question,
        results
    )

    gap_prompt = build_gap_prompt(
        research_context
    )

    answer = generate_answer(
        gap_prompt
    )

    return {
        "question": question,
        "answer": answer,
        "research_context": research_context,
        "sources": research_context["evidence"],
        "paper_count": research_context["paper_count"],
        "evidence_count": research_context["evidence_count"]
    }


if __name__ == "__main__":

    question = """
    What research gaps and future research directions
    are identified regarding generative AI in education?
    """

    result = gap_agent(
        question,
        top_k=5
    )

    print("\n========================================")
    print("             GAP AGENT")
    print("========================================")

    print("\nResearch Question:")
    print(result["question"])

    print("\nPapers Available:")
    print(result["paper_count"])

    print("\nEvidence Retrieved:")
    print(result["evidence_count"])

    print("\n========================================")
    print("           RESEARCH GAPS")
    print("========================================")

    print(result["answer"])

    print("\n========================================")
    print("              SOURCES")
    print("========================================")

    for source in result["sources"]:

        print(
            f"\n[{source['source_number']}] "
            f"{source['title']} ({source['year']})"
        )

        print("Section:", source["section"])
        print("Chunk:", source["chunk_id"])

    print("\n========================================")