from pdf_extractor import extract_text_from_pdf
from text_cleaner import clean_text
from text_chunker import parse_sections, create_chunks
from sentence_transformers import SentenceTransformer
from vector_store import create_vector_store


MODEL_NAME = "all-MiniLM-L6-v2"


def process_one_paper(pdf_path, paper_metadata):

    print("\n========================================")
    print("         PROCESSING RESEARCH PAPER")
    print("========================================")

    # -------------------------------------
    # 1. Extract PDF text
    # -------------------------------------
    print("\n[1] Extracting PDF text...")

    text = extract_text_from_pdf(str(pdf_path))

    print("Extracted characters:", len(text))

    # -------------------------------------
    # 2. Clean text
    # -------------------------------------
    print("\n[2] Cleaning text...")

    cleaned_text = clean_text(text)

    print("Cleaned characters:", len(cleaned_text))

    # -------------------------------------
    # 3. Parse sections
    # -------------------------------------
    print("\n[3] Parsing sections...")

    sections = parse_sections(cleaned_text)

    print("Sections detected:", len(sections))

    # -------------------------------------
    # 4. Create chunks
    # -------------------------------------
    print("\n[4] Creating chunks...")

    chunks = create_chunks(
        sections,
        paper_metadata,
        max_words=400,
        overlap_words=80
    )

    print("Chunks created:", len(chunks))

    # -------------------------------------
    # 5. Create embeddings
    # -------------------------------------
    print("\n[5] Creating embeddings...")

    model = SentenceTransformer(MODEL_NAME)

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    print("Embedding dimension:", len(embeddings[0]))

    # -------------------------------------
    # 6. Store vectors in Qdrant
    # -------------------------------------
    print("\n[6] Storing vectors in Qdrant...")

    create_vector_store(chunks, embeddings)

    print("\n========================================")
    print("         PAPER INGESTION COMPLETE")
    print("========================================")

    return {
        "paper": paper_metadata,
        "chunks": chunks
    }


if __name__ == "__main__":
    print("paper_pipeline.py loaded successfully.")