from semantic_search import search_papers, build_research_context
from llm_client import generate_answer


def build_analysis_prompt(question, research_context):

    prompt = f"""
You are a research analysis assistant.

Your task is to answer the user's research question
using only the research evidence provided below.

IMPORTANT RULES:

1. Use only the provided research evidence.
2. Do not invent facts or sources.
3. Clearly distinguish evidence from interpretation.
4. When making an important claim, identify the supporting source.
5. If the evidence is insufficient, say so.
6. Prefer evidence from the retrieved papers.
7. Do not introduce outside knowledge.

RESEARCH QUESTION:
{question}

RETRIEVED RESEARCH EVIDENCE:
"""

    for source in research_context:

        prompt += f"""
SOURCE {source['source_number']}

Title:
{source['title']}

Year:
{source['year']}

Section:
{source['section']}

DOI:
{source['doi']}

Relevance Score:
{source['relevance_score']}

Evidence:
{source['text']}

----------------------------------------
"""

    prompt += """

ANALYSIS TASK:

Based only on the retrieved evidence:

1. Identify the main findings relevant to the question.
2. Compare the evidence across sources where possible.
3. Identify important limitations or uncertainties.
4. Provide a concise research-oriented synthesis.
5. Cite the source number for important claims.

Do not introduce information that is not supported
by the retrieved evidence.
"""

    return prompt


def research_agent(question, top_k=5):

    # Step 1: Retrieve relevant chunks from Qdrant
    results = search_papers(question, top_k=top_k)

    # Step 2: Convert retrieved results into research context
    research_context = build_research_context(results)

    # Step 3: Build evidence-based prompt
    analysis_prompt = build_analysis_prompt(
        question,
        research_context
    )

    # Step 4: Send prompt to Gemini
    answer = generate_answer(analysis_prompt)

    return {
        "question": question,
        "sources": research_context,
        "answer": answer
    }


if __name__ == "__main__":

    question = "How can generative AI support learning and education?"

    research_result = research_agent(
        question,
        top_k=3
    )

    print("\n===== RESEARCH AGENT =====")

    print("\nResearch Question:")
    print(research_result["question"])

    print("\nSources Retrieved:")
    print(len(research_result["sources"]))

    print("\n===== GEMINI RESEARCH ANALYSIS =====")
    print(research_result["answer"])

    print("\n===== SOURCES USED =====")

    for source in research_result["sources"]:

        print(
            f"\n[{source['source_number']}] "
            f"{source['title']} "
            f"({source['year']})"
        )

    print("\n===== END RESEARCH AGENT =====")