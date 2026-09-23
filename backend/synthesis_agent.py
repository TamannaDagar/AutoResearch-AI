from semantic_search import (
    search_papers,
    build_research_context
)

from llm_client import generate_answer


def build_synthesis_prompt(research_context):

    question = research_context["question"]
    papers = research_context["papers"]
    evidence = research_context["evidence"]

    prompt = f"""
You are a research synthesis assistant.

Your task is to produce a coherent research synthesis
from the provided research evidence.

Use ONLY the research context provided below.

IMPORTANT RULES:

1. Do not introduce outside knowledge.
2. Do not invent findings, claims, or sources.
3. Base important statements on the retrieved evidence.
4. Clearly distinguish direct evidence from interpretation.
5. Identify the source number supporting important claims.
6. Do not treat relevance scores as evidence.
7. Do not assume that one paper represents the entire
   research field.
8. If the evidence is limited, explicitly state the limitation.
9. Do not convert absence of evidence into evidence of absence.
10. Preserve uncertainty where the research evidence is uncertain.

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

RESEARCH EVIDENCE:

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
SYNTHESIS TASK:

Based ONLY on the provided evidence:

1. Provide a concise overview of what the evidence
   says about the research question.

2. Identify the major findings supported by the evidence.

3. Identify important benefits or positive findings
   where supported.

4. Identify important challenges, limitations, or risks
   where supported.

5. Identify future research directions where explicitly
   supported.

6. Explain relationships between the findings when the
   evidence supports them.

7. Clearly identify important uncertainties and evidence
   limitations.

8. Provide source numbers for important claims.

9. Do not claim that the findings represent the entire
   research field when the corpus is limited.

10. End with a short statement describing what additional
    evidence would be needed for a stronger synthesis.

Produce a concise, research-oriented synthesis.
"""

    return prompt


def synthesis_agent(question, top_k=5):

    results = search_papers(
        question,
        top_k=top_k
    )

    research_context = build_research_context(
        question,
        results
    )

    synthesis_prompt = build_synthesis_prompt(
        research_context
    )

    answer = generate_answer(
        synthesis_prompt
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
    What does the available research evidence indicate
    about the benefits, challenges, and future directions
    of generative AI in higher education?
    """

    result = synthesis_agent(
        question,
        top_k=5
    )

    print("\n========================================")
    print("          SYNTHESIS AGENT")
    print("========================================")

    print("\nResearch Question:")
    print(result["question"])

    print("\nPapers Available:")
    print(result["paper_count"])

    print("\nEvidence Retrieved:")
    print(result["evidence_count"])

    print("\n========================================")
    print("        RESEARCH SYNTHESIS")
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