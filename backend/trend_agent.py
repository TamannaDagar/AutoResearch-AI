from semantic_search import (
    search_papers,
    build_research_context
)

from llm_client import generate_answer


def build_trend_prompt(research_context):

    question = research_context["question"]
    papers = research_context["papers"]
    evidence = research_context["evidence"]

    prompt = f"""
You are a research trend analysis assistant.

Your task is to identify research trends and patterns
from the research papers and evidence provided below.

Use ONLY the provided research context.

IMPORTANT RULES:

1. Do not introduce outside knowledge.
2. Do not invent publication trends.
3. Do not claim that a trend exists based on a single paper.
4. Distinguish observations from interpretations.
5. Use publication years only when they are provided.
6. Identify recurring research themes only when supported
   by the provided evidence.
7. Clearly state when the corpus is too small to establish
   a reliable research trend.
8. Do not treat relevance scores as evidence.
9. Cite the source number for evidence-based observations.

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

Evidence:
{source["text"]}

----------------------------------------
"""

    prompt += """
TREND ANALYSIS TASK:

Based ONLY on the provided research context:

1. Identify the publication years represented in
   the available papers.

2. Identify recurring research themes supported
   by the evidence.

3. Identify emerging topics only when the evidence
   supports them.

4. Identify methodological patterns where supported.

5. Identify changes over time only if papers from
   different years provide enough evidence.

6. Clearly distinguish:
   - Direct observation
   - Evidence-based interpretation
   - Insufficient evidence

7. If only one paper is available, explicitly state
   that a reliable publication trend cannot be established.

8. Do not invent missing years, topics, methods,
   or research directions.

Provide a concise research trend analysis.
"""

    return prompt


def trend_agent(question, top_k=5):

    results = search_papers(
        question,
        top_k=top_k
    )

    research_context = build_research_context(
        question,
        results
    )

    trend_prompt = build_trend_prompt(
        research_context
    )

    answer = generate_answer(
        trend_prompt
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
    What research trends can be identified in the study
    of generative AI in education?
    """

    result = trend_agent(
        question,
        top_k=5
    )

    print("\n========================================")
    print("            TREND AGENT")
    print("========================================")

    print("\nResearch Question:")
    print(result["question"])

    print("\nPapers Available:")
    print(result["paper_count"])

    print("\nEvidence Retrieved:")
    print(result["evidence_count"])

    print("\n========================================")
    print("          RESEARCH TRENDS")
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