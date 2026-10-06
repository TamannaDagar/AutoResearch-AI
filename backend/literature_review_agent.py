"""
Literature Review Agent

Generates a structured, research-oriented literature review
from semantically retrieved research-paper evidence.

The agent:
1. Retrieves evidence from the current paper set.
2. Ensures paper diversity.
3. Organizes the evidence paper-by-paper.
4. Synthesizes major themes across studies.
5. Identifies agreements, differences, and limitations.
6. Extracts research gaps only when supported by evidence.
7. Suggests future research directions grounded in the corpus.
"""

from semantic_search import search_papers
from llm_client import generate_answer


def build_literature_review_context(results):
    """
    Convert Qdrant ScoredPoint results into structured context
    for Gemini.
    """

    if not results:
        return "No relevant research evidence was retrieved."

    context_parts = []

    for i, result in enumerate(results, start=1):

        payload = result.payload or {}

        title = payload.get("title", "Unknown title")
        year = payload.get("year", "Unknown year")
        section = payload.get("section", "Unknown section")
        chunk_id = payload.get("chunk_id", "Unknown chunk")
        text = payload.get("text", "")

        context_parts.append(
            f"""
SOURCE {i}

Title: {title}
Year: {year}
Section: {section}
Chunk: {chunk_id}

Evidence:
{text}
"""
        )

    return "\n".join(context_parts)


def literature_review_agent(
    research_question,
    top_k=5,
    paper_ids=None
):
    """
    Generate a research-oriented literature review.

    Parameters
    ----------
    research_question : str
        The research question/topic for the review.

    top_k : int
        Maximum number of papers/evidence items to retrieve.

    paper_ids : list[str] or None
        Optional list of OpenAlex paper IDs representing
        the current research run.

        If provided, retrieval is restricted to these papers.
        If None, the complete persistent Qdrant corpus is searched.

    Returns
    -------
    str
        Generated literature review.
    """

    # =========================================================
    # 1. RETRIEVE RELEVANT EVIDENCE
    # =========================================================

    results = search_papers(
        research_question,
        top_k=top_k,
        one_result_per_paper=True,
        paper_ids=paper_ids
    )

    if not results:
        return (
            "No relevant research evidence was found for the "
            "provided research question."
        )

    # =========================================================
    # 2. BUILD EVIDENCE CONTEXT
    # =========================================================

    context = build_literature_review_context(results)

    # =========================================================
    # 3. ACADEMIC LITERATURE REVIEW PROMPT
    # =========================================================

    prompt = f"""
You are an academic literature-review assistant.

Your task is to write a rigorous, research-oriented literature
review using ONLY the research evidence provided below.

Research Question:

{research_question}

============================================================
RETRIEVED RESEARCH EVIDENCE
============================================================

{context}

============================================================
IMPORTANT EVIDENCE RULES
============================================================

1. Use ONLY the information contained in the retrieved evidence.

2. Do NOT invent:
   - methodologies
   - sample sizes
   - participant characteristics
   - statistical results
   - research findings
   - research gaps
   - future-work recommendations

3. If a paper's methodology, population, or findings are not
   explicitly available in the retrieved evidence, say that the
   information is not available rather than guessing.

4. Distinguish clearly between:

   - what the source explicitly reports
   - synthesis across multiple sources
   - reasonable interpretation

5. Do not assume that all papers use the same research design.

6. Where possible, distinguish between:

   - empirical studies
   - systematic reviews
   - conceptual papers
   - theoretical discussions

7. Do not claim that a finding applies universally when the
   evidence comes from a limited context.

8. If the retrieved evidence is insufficient to establish a
   research gap or future research direction, explicitly state
   this limitation.

9. Every major claim should be connected to one or more source
   numbers such as [1], [2], [3].

10. Do not use information from your general knowledge that is
    absent from the retrieved evidence.

============================================================
LITERATURE REVIEW STRUCTURE
============================================================

Write the literature review using the following structure.

# Literature Review: Generative AI in Higher Education

## 1. Introduction

Introduce the research topic and explain its importance based
only on the retrieved literature.

Briefly establish the scope of the retrieved evidence.

Do not introduce unsupported background information.

---

## 2. Overview of the Retrieved Literature

Provide a concise synthesis of what the retrieved papers
contribute to the topic.

Discuss the papers in relation to one another rather than
producing five disconnected summaries.

Where supported by the evidence, identify:

- research focus
- educational context
- population
- type of contribution
- major findings
- major arguments

If this information is unavailable, do not guess.

---

## 3. Major Themes in the Literature

Identify the major themes emerging across the papers.

For every major theme:

### 3.1 [Theme Name]

Explain the theme and synthesize evidence from multiple
papers where possible.

Discuss whether the papers:

- reach similar conclusions
- emphasize different aspects
- provide complementary evidence
- leave the issue uncertain

Use citations such as [1, 2, 4].

Do not simply list individual paper findings.

---

## 4. Benefits and Opportunities

Synthesize the benefits and opportunities reported in the
retrieved literature.

Possible themes may include, ONLY when supported by the evidence:

- personalized learning
- teaching and learning support
- writing and brainstorming
- research assistance
- assessment and feedback
- efficiency
- student engagement

For each important benefit, explain:

1. Which papers report it.
2. What the evidence actually states.
3. Whether the evidence appears empirical, conceptual,
   or review-based when this can be established.
4. Whether the evidence is consistent across papers.

Avoid exaggerated language.

---

## 5. Challenges, Risks, and Limitations

Synthesize the major challenges reported by the literature.

Possible categories may include:

- academic integrity
- authenticity of student work
- overreliance on AI
- cognitive or skill development
- privacy
- bias
- ethical concerns
- regulatory challenges
- inequality or access

Only include categories supported by the retrieved evidence.

For each major challenge, compare the evidence across papers.

Clearly distinguish between:

- directly reported concerns
- broader interpretations
- unresolved issues

---

## 6. Student Perspectives and Perceptions

Where the retrieved evidence contains student perspectives,
analyze them separately.

Discuss, when supported:

- attitudes
- perceived benefits
- perceived challenges
- willingness to use GenAI
- concerns about GenAI

Do not attribute researcher or institutional perspectives
to students.

If the evidence does not contain enough student-specific
information, explicitly state this.

---

## 7. Cross-Paper Comparison and Synthesis

This is a critical section.

Do NOT simply summarize the papers again.

Instead discuss:

### Areas of Agreement

What findings, opportunities, or concerns appear across
multiple papers?

### Differences

Where do papers differ in:

- emphasis
- educational context
- perspective
- conclusions
- type of evidence?

### Complementary Findings

How do different papers contribute different pieces of
understanding to the same research problem?

### Evidence Strength and Uncertainty

Where is the evidence relatively strong?

Where is the evidence limited?

Do not make unsupported judgments about evidence quality.

---

## 8. Research Gaps

Identify research gaps ONLY when they are supported by
the retrieved literature.

Potential gaps may include:

- underrepresented populations
- underexplored educational contexts
- unresolved contradictions
- methodological limitations
- insufficient empirical evidence
- repeatedly identified areas requiring investigation

Do NOT invent research gaps.

If explicit research gaps are not present, state:

"The retrieved evidence does not provide enough information
to identify specific standalone research gaps."

You may then identify cautious areas requiring further
investigation, but clearly label them as evidence-based
interpretations rather than explicit claims from the papers.

---

## 9. Future Research Directions

Discuss future research directions only when supported
by the retrieved evidence.

Clearly distinguish between:

### Explicit Future Directions

Directions directly mentioned in the retrieved literature.

### Evidence-Based Directions

Potential directions that can reasonably be inferred from
limitations or unresolved issues explicitly present in the
retrieved evidence.

Do not present your own ideas as if they came directly
from the papers.

---

## 10. Overall Synthesis

Provide a concise academic synthesis of the literature.

Directly answer the research question.

Explain:

- what the literature generally agrees on
- the main benefits
- the major challenges
- important differences between perspectives
- what remains uncertain
- the overall state of the retrieved evidence

Do not simply repeat earlier sections.

---

## 11. Limitations of This Literature Review

Clearly state limitations caused by the retrieved evidence.

Consider:

- number of papers
- diversity of contexts
- missing methodology details
- missing full-text sections
- limited student-specific evidence
- differences in research design
- limitations of the retrieved corpus

Do not claim that this review represents the entire academic
field unless the evidence supports such a conclusion.

============================================================
ACADEMIC WRITING STYLE
============================================================

Use a formal academic writing style appropriate for a
university-level literature review.

The writing should emphasize SYNTHESIS rather than
simple paper-by-paper summarization.

Use paragraphs for important analytical discussion.

Use headings and subheadings for readability.

Prefer language such as:

"the literature suggests..."

"several studies report..."

"the retrieved evidence indicates..."

"the findings are broadly consistent..."

"the studies differ in..."

"the evidence remains limited..."

"the retrieved literature does not establish..."

Avoid:

- marketing language
- exaggerated claims
- unsupported conclusions
- repetitive statements
- generic explanations unrelated to the retrieved evidence

============================================================
CITATION RULE
============================================================

Use the source numbers exactly as provided.

Example:

Several studies identify personalized learning and adaptive
feedback as important opportunities associated with GenAI [1, 2, 4].

If a claim comes from only one source:

The study reports positive student attitudes toward GenAI [3].

Do not create citations that are not represented in the
retrieved evidence.

============================================================

Now write the complete literature review.
"""

    # =========================================================
    # 4. GENERATE REVIEW USING EXISTING LLM CLIENT
    # =========================================================

    review = generate_answer(prompt)

    return review


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("       LITERATURE REVIEW AGENT")
    print("========================================")

    research_question = """
Provide a literature review of research on generative AI
in higher education, focusing on benefits, challenges,
student perceptions, and future research directions.
"""

    # Current research-run papers.
    #
    # These IDs correspond to the papers currently present
    # in accessible_papers.json.

    current_paper_ids = [
        "https://openalex.org/W4384464487",
        "https://openalex.org/W4411842024",
        "https://openalex.org/W4379046986",
        "https://openalex.org/W4404509460",
        "https://openalex.org/W4406199489",
    ]

    result = literature_review_agent(
        research_question,
        top_k=5,
        paper_ids=current_paper_ids
    )

    print("\n========================================")
    print("          LITERATURE REVIEW")
    print("========================================")

    print(result)

    print("\n========================================")
    print("              SOURCES")
    print("========================================")

    # Retrieve the same evidence again only for displaying
    # the source list.

    results = search_papers(
        research_question,
        top_k=5,
        one_result_per_paper=True,
        paper_ids=current_paper_ids
    )

for i, result in enumerate(results, start=1):

    payload = result.payload or {}

    print(
        f"\n[{i}] {payload.get('title', 'Unknown title')} "
        f"({payload.get('year', 'Unknown year')})"
    )

    print(
        f"Section: {payload.get('section', 'Unknown section')}"
    )

    print(
        f"Chunk: {payload.get('chunk_id', 'Unknown chunk')}"
    )