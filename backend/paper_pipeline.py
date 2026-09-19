from pathlib import Path
import json

from pdf_extractor import extract_text_from_pdf
from text_cleaner import clean_text
from text_chunker import parse_sections, create_chunks
from sentence_transformers import SentenceTransformer
from vector_store import create_vector_store
from research_agent import research_agent


MODEL_NAME = "all-MiniLM-L6-v2"


def process_one_paper(
    pdf_path,
    paper_metadata,
    question
):
    """
    Process one research paper through the complete pipeline.
    """

    print("\n========================================")
    print("         PROCESSING RESEARCH PAPER")
    print("========================================")

    # ------------------------------------
    # 1. Extract PDF text
    # ------------------------------------

    print("\n[1] Extracting PDF text...")

    text = extract_text_from_pdf(str(pdf_path))

    print("Extracted characters:", len(text))

    # ------------------------------------
    # 2. Clean text
    # ------------------------------------

    print("\n[2] Cleaning text...")

    cleaned_text = clean_text(text)

    print("Cleaned characters:", len(cleaned_text))

    # ------------------------------------
    # 3. Parse sections
    # ------------------------------------

    print("\n[3] Parsing sections...")

    sections = parse_sections(cleaned_text)

    print("Sections detected:", len(sections))

    # ------------------------------------
    # 4. Create chunks
    # ------------------------------------

    print("\n[4] Creating chunks...")

    chunks = create_chunks(
        sections,
        paper_metadata,
        max_words=400,
        overlap_words=80
    )

    print("Chunks created:", len(chunks))

    # ------------------------------------
    # 5. Create embeddings
    # ------------------------------------

    print("\n[5] Creating embeddings...")

    model = SentenceTransformer(MODEL_NAME)

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    print("Embedding dimension:", len(embeddings[0]))

    # ------------------------------------
    # 6. Store in Qdrant
    # ------------------------------------

    print("\n[6] Storing vectors in Qdrant...")

    create_vector_store(
        chunks,
        embeddings
    )

    # ------------------------------------
    # 7. Research analysis
    # ------------------------------------

    print("\n[7] Running research agent...")

    research_result = research_agent(
        question,
        top_k=3
    )

    print("\n========================================")
    print("         PAPER PROCESSING COMPLETE")
    print("========================================")

    return {
        "paper": paper_metadata,
        "chunks": chunks,
        "research_result": research_result
    }

if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent

    PDF_FILE = (
        BASE_DIR
        / "data"
        / "papers"
        / "pdfs"
        / "test_paper.pdf"
    )

    METADATA_FILE = (
        BASE_DIR
        / "data"
        / "papers"
        / "cleaned_papers.json"
    )

    with open(METADATA_FILE, "r", encoding="utf-8") as file:
        papers = json.load(file)

    test_title = (
        "Towards social generative AI for education: "
        "theory, practices and ethics"
    )

    paper_metadata = None

    for paper in papers:
        if paper.get("title") == test_title:
            paper_metadata = paper
            break

    if paper_metadata is None:
        raise ValueError(
            "Test paper metadata not found."
        )

    question = (
        "How can generative AI support learning and education?"
    )

    result = process_one_paper(
        pdf_path=PDF_FILE,
        paper_metadata=paper_metadata,
        question=question
    )

    print("\n===== FINAL RESEARCH ANSWER =====")
    print(result["research_result"]["answer"])

    print("\n===== SOURCES =====")

    for source in result["research_result"]["sources"]:
        print(
            f"[{source['source_number']}] "
            f"{source['title']}"
        )