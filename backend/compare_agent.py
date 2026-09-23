from semantic_search import (
    search_papers, build_research_context
)

from llm_client import generate_answer

def build_compare_prompt(research_context):
    question = research_context["question"]
    papers = research_context["papers"]
    evidence = research_context["evidence"]


    prompt = f"""
You are a research comparison assistant.

Your task is to compare the research papers represented
in the provided research context.

Use ONLY the provided research evidence.

IMPORTANT RULES:

1. Do not invent facts about any paper.
2. Do not use outside knowledge.
3. Only compare information supported by the evidence.
4. Do not treat relevance scores as evidence.
5. Clearly distinguish direct evidence from interpretation.
6. If there are not enough papers for comparison, explicitly say so.
7. Do not assume that papers have similar methods or findings
   unless the evidence supports that conclusion.

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

RETRIEVED EVIDENCE:

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
COMPARISON TASK:

Based ONLY on the available evidence:

1. Identify the papers available for comparison.
2. Compare their research focus where evidence is available.
3. Compare their methodologies where evidence is available.
4. Compare their major findings where evidence is available.
5. Compare limitations where evidence is available.
6. Identify similarities between papers.
7. Identify differences between papers.
8. State clearly when the available evidence is insufficient.
9. Do not invent missing information.

Provide a concise research-oriented comparison.
"""

    return prompt


def compare_agent(question, top_k=5):

    results = search_papers(
        question,
        top_k=top_k
    )

    research_context = build_research_context(
        question,
        results
    )

    comparison_prompt = build_compare_prompt(
        research_context
    )

    answer = generate_answer(
        comparison_prompt
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
    How do research studies describe the benefits
    and challenges of generative AI in education?
    """

    result = compare_agent(
        question,
        top_k=5
    )

    print("\n========================================")
    print("           COMPARE AGENT")
    print("========================================")

    print("\nResearch Question:")
    print(result["question"])

    print("\nPapers Available:")
    print(result["paper_count"])

    print("\nEvidence Retrieved:")
    print(result["evidence_count"])

    print("\n========================================")
    print("          PAPER COMPARISON")
    print("========================================")

    print(result["answer"])

    print("\n========================================")
    print("             SOURCES")
    print("========================================")

    for source in result["sources"]:

        print(
            f"\n[{source['source_number']}] "
            f"{source['title']} ({source['year']})"
        )

        print("Section:", source["section"])
        print("Chunk:", source["chunk_id"])

    print("\n========================================")