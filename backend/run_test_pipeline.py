from pathlib import Path
import json

from pdf_extractor import extract_text_from_pdf
from text_cleaner import clean_text
from text_chunker import create_chunks, parse_sections

from sentence_transformers import SentenceTransformer
from vector_store import create_vector_store

BASE_DIR= Path(__file__).resolve().parent.parent

PDF_FILE= BASE_DIR/ "data"/ "papers"/ "pdfs"/ "test_paper.pdf"
TEXT_FILE = BASE_DIR / "data" / "papers" / "text" / "test_paper_pipeline.txt"
CLEANED_TEXT_FILE = (
    BASE_DIR / "data" / "papers" / "text" / "test_paper_pipeline_cleaned.txt"
)
CHUNKS_FILE = (
    BASE_DIR / "data" / "papers" / "chunks" / "test_paper_chunks.json"
)

METADATA_FILE = (
    BASE_DIR / "data" / "papers" / "cleaned_papers.json"
)

def run_pipeline():

    print("\n========================================")
    print("      AUTORESEARCH AI TEST PIPELINE")
    print("========================================")

    # STEP 1 — Check PDF
    print("\n[1/3] Checking test PDF...")

    if not PDF_FILE.exists():
        raise FileNotFoundError(
            f"Test PDF not found:\n{PDF_FILE}"
        )

    print("PDF found:", PDF_FILE)


    # STEP 2 — Extract text
    print("\n[2/3] Extracting text from PDF...")

    text = extract_text_from_pdf(str(PDF_FILE))

    print("Extracted characters:", len(text))

    TEXT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(TEXT_FILE, "w", encoding="utf-8") as file:
        file.write(text)

    print("Raw text saved to:", TEXT_FILE)


    # STEP 3 — Clean text
    print("\n[3/3] Cleaning extracted text...")

    cleaned_text = clean_text(text)

    with open(CLEANED_TEXT_FILE, "w", encoding="utf-8") as file:
        file.write(cleaned_text)

    print("Cleaned text saved to:", CLEANED_TEXT_FILE)

    print("\n========================================")
    print("       PREPROCESSING COMPLETED")
    print("========================================")


    print("\n[4/4] Creating research chunks...")

    with open(METADATA_FILE, "r", encoding="utf-8") as file:
        papers = json.load(file)

    test_title = "Towards social generative AI for education: theory, practices and ethics"

    paper_metadata = None

    for paper in papers:
        if paper.get("title") == test_title:
            paper_metadata = paper
            break

    if paper_metadata is None:
        raise ValueError(
            "Test paper metadata not found in cleaned_papers.json"
        )

    sections = parse_sections(cleaned_text)

    print("Sections detected:", len(sections))

    chunks = create_chunks(
        sections,
        paper_metadata,
        max_words=400,
        overlap_words=80
    )

    CHUNKS_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(CHUNKS_FILE, "w", encoding="utf-8") as file:
        json.dump(chunks, file, indent=2, ensure_ascii=False)

    print("Chunks created:", len(chunks))
    print("Chunks saved to:", CHUNKS_FILE)


    print("\n[5/5] Creating embeddings...")

    MODEL_NAME = "all-MiniLM-L6-v2"

    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    print("Embeddings created:", len(embeddings))
    print("Embedding dimension:", len(embeddings[0]))

    create_vector_store(
        chunks,
        embeddings
    )

    print("\n========================================")
    print("       TEST PAPER PIPELINE COMPLETE")
    print("========================================")


if __name__ == "__main__":
    run_pipeline()
