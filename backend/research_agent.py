from semantic_search import(
    search_papers,
    build_research_context
)

# --------------------------------------------------
# Build Research Analysis Prompt
# --------------------------------------------------
def build_analysis_prompt(
    question,
    research_context
):
    """
    Create an evidence-grounded prompt for the
    future LLM research analysis layer.
    """

    prompt = f"""
You are a research analysis assistant.

Your task is to analyze the research evidence
provided below and answer the user's research
question.

IMPORTANT RULES:

1. Use only the provided research evidence.
2. Do not invent facts or sources.
3. Clearly distinguish evidence from interpretation.
4. When making a claim, identify the supporting source.
5. If the evidence is insufficient, say so.
6. Prefer evidence from the retrieved papers rather
   than general knowledge.

   
RESEARCH QUESTION:
{question}

RETRIEVED RESEARCH EVIDENCE:
"""

    for source in research_context:

        prompt += f"""

SOURCE {source['source_number']}
Title: {source['title']}
Year: {source['year']}
Section: {source['section']}
DOI: {source['doi']}
Relevance Score: {source['relevance_score']}

Evidence:
{source['text']}
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


# --------------------------------------------------
# Research Agent
# --------------------------------------------------

def research_agent(
    question,
    top_k=5
):
    """
    Retrieve research evidence and prepare it
    for analysis by an LLM.
    """

    # ----------------------------------------------
    # Step 1: Retrieve relevant research
    # ----------------------------------------------

    results = search_papers(
        question,
        top_k=top_k
    )

    # ----------------------------------------------
    # Step 2: Build structured research context
    # ----------------------------------------------

    research_context = build_research_context(
        results
    )

    # ----------------------------------------------
    # Step 3: Build analysis prompt
    # ----------------------------------------------

    analysis_prompt = build_analysis_prompt(
        question,
        research_context
    )

    return {
        "question": question,
        "sources": research_context,
        "prompt": analysis_prompt
    }


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    question = (
        "How can generative AI "
        "support learning and education?"
    )

    research_result = research_agent(
        question,
        top_k=3
    )

    print(
        "\n===== RESEARCH AGENT ====="
    )

    print(
        "\nResearch Question:"
    )

    print(
        research_result["question"]
    )

    print(
        "\nSources Retrieved:",
        len(research_result["sources"])
    )

    print(
        "\n===== GENERATED ANALYSIS PROMPT ====="
    )

    print(
        research_result["prompt"]
    )

    print(
        "\n===== END RESEARCH AGENT ====="
    )    