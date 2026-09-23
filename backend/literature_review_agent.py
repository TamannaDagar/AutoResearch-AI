from semantic_search import (
    search_papers,
    build_research_context
)

from llm_client import generate_answer


def build_literature_review_prompt(research_context):

    question = research_context["question"]
    papers = research_context["papers"]
    evidence = research_context["evidence"]

    prompt = f"""
You are a research literature review assistant.

Your task is to produce a structured literature review
based ONLY on the research evidence provided below.

IMPORTANT RULES:

1. Use only the provided research evidence.
2. Do not introduce outside knowledge.
3. Do not invent studies, findings, authors, methods,
   or research gaps.
4. Clearly distinguish evidence from interpretation.
5. Cite source numbers for important claims.
6. Do not treat relevance scores as evidence.
7. Do not assume that one paper represents the entire
   research field.
8. If the available literature is limited, explicitly
   state the limitation.
9. Do not treat references cited inside a paper as
   independent papers in the research corpus.
10. Preserve uncertainty where evidence is insufficient.

RESEARCH QUESTION:

{question}


RESEARCH PAPERS IN THE CURRENT CORPUS:

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

Evidence:
{source["text"]}

----------------------------------------
"""

    prompt += """
LITERATURE REVIEW TASK:

Produce a structured literature review containing:

1. INTRODUCTION
   - Introduce the research topic using only the
     available evidence.

2. MAJOR RESEARCH THEMES
   - Identify the major themes represented in the
     available research evidence.

3. FINDINGS
   - Summarize important findings associated with
     each theme.
   - Cite the supporting source numbers.

4. BENEFITS AND OPPORTUNITIES
   - Summarize benefits supported by the evidence.

5. CHALLENGES AND LIMITATIONS
   - Summarize challenges, risks, and limitations
     supported by the evidence.

6. RESEARCH GAPS
   - Include only explicitly supported research gaps
     or future research directions.

7. FUTURE RESEARCH
   - Summarize explicitly stated future research
     directions.

8. OVERALL SYNTHESIS
   - Connect the themes and findings into a coherent
     research narrative.

9. EVIDENCE LIMITATIONS
   - Explain limitations of the current research corpus.
   - State clearly when the available evidence is
     insufficient for broader conclusions.

IMPORTANT:

The current corpus may contain fewer papers than a
complete literature review would normally require.

Do not pretend that the available corpus represents
the complete research literature.

Do not use references cited inside a paper as separate
research studies unless those papers have independently
been retrieved into the research corpus.

Produce an academic, concise, evidence-grounded
literature review.
"""

    return prompt


def literature_review_agent(
    question,
    top_k=5
):

    results = search_papers(
        question,
        top_k=top_k
    )

    research_context = build_research_context(
        question,
        results
    )

    literature_review_prompt = build_literature_review_prompt(
        research_context
    )

    answer = generate_answer(
        literature_review_prompt
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
    Provide a literature review of research on
    generative AI in higher education, focusing on
    benefits, challenges, student perceptions,
    and future research directions.
    """

    result = literature_review_agent(
        question,
        top_k=5
    )

    print("\n========================================")
    print("       LITERATURE REVIEW AGENT")
    print("========================================")

    print("\nResearch Question:")
    print(result["question"])

    print("\nPapers Available:")
    print(result["paper_count"])

    print("\nEvidence Retrieved:")
    print(result["evidence_count"])

    print("\n========================================")
    print("          LITERATURE REVIEW")
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