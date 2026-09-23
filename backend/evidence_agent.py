from semantic_search import (
    search_papers,
    build_research_context
)

from llm_client import generate_answer


def build_evidence_prompt(research_context):

    question = research_context["question"]
    papers = research_context["papers"]
    evidence = research_context["evidence"]

    prompt = f"""
You are a research evidence verification assistant.

Your task is to identify important claims from the
retrieved research evidence and connect each claim
to its supporting source.

Use ONLY the evidence provided below.

IMPORTANT RULES:

1. Do not introduce outside knowledge.
2. Do not invent claims.
3. Every important claim must be connected to
   a specific evidence source.
4. Preserve the meaning of the original evidence.
5. Do not treat relevance scores as evidence.
6. Clearly distinguish direct evidence from interpretation.
7. If a claim cannot be directly supported by the
   retrieved evidence, mark it as insufficiently supported.
8. Use the source number when referencing evidence.

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

Relevance Score:
{source["relevance_score"]}

Evidence:
{source["text"]}

----------------------------------------
"""

    prompt += """
EVIDENCE VERIFICATION TASK:

Based ONLY on the retrieved evidence:

1. Identify the important research claims supported
   by the evidence.

2. For each claim, provide:
   - Claim
   - Evidence
   - Source number
   - Paper title
   - Section
   - Chunk ID

3. Explain briefly why the evidence supports the claim.

4. Identify claims that appear in the evidence but
   cannot be sufficiently supported.

5. Clearly distinguish:
   - Directly supported claim
   - Evidence-based interpretation
   - Insufficiently supported claim

6. Do not combine unrelated evidence into one claim.

7. Do not introduce information that is not present
   in the retrieved research evidence.

Return a concise evidence verification report.
"""

    return prompt


def evidence_agent(question, top_k=5):

    results = search_papers(
        question,
        top_k=top_k
    )

    research_context = build_research_context(
        question,
        results
    )

    evidence_prompt = build_evidence_prompt(
        research_context
    )

    answer = generate_answer(
        evidence_prompt
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
    What evidence supports the benefits and challenges
    of generative AI in higher education?
    """

    result = evidence_agent(
        question,
        top_k=5
    )

    print("\n========================================")
    print("          EVIDENCE AGENT")
    print("========================================")

    print("\nResearch Question:")
    print(result["question"])

    print("\nPapers Available:")
    print(result["paper_count"])

    print("\nEvidence Retrieved:")
    print(result["evidence_count"])

    print("\n========================================")
    print("        EVIDENCE VERIFICATION")
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