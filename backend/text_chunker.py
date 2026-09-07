from pathlib import Path
import json
import re


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Input and output paths
INPUT_FILE = BASE_DIR / "data" / "papers" / "text" / "test_paper_cleaned.txt"
OUTPUT_FILE = BASE_DIR / "data" / "papers" / "chunks" / "test_paper_chunks.json"


def split_into_paragraphs(text):
    """
    Split cleaned text into paragraphs.
    """

    paragraphs = re.split(r"\n\s*\n", text)

    paragraphs = [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip()
    ]

    return paragraphs


def create_chunks(paragraphs, max_words=400, overlap_words=80):
    """
    Create overlapping chunks while trying to preserve paragraph boundaries.
    """

    chunks = []

    current_chunk = []
    current_word_count = 0

    for paragraph in paragraphs:

        paragraph_words = paragraph.split()
        paragraph_word_count = len(paragraph_words)

        # If adding this paragraph exceeds the limit,
        # save the current chunk first.
        if (
            current_chunk
            and current_word_count + paragraph_word_count > max_words
        ):

            chunk_text = " ".join(current_chunk)

            chunks.append(chunk_text)

            # Keep the last few words for overlap
            overlap_text = chunk_text.split()[-overlap_words:]

            current_chunk = [" ".join(overlap_text)]
            current_word_count = len(overlap_text)

        current_chunk.append(paragraph)
        current_word_count += paragraph_word_count

    # Save remaining text
    if current_chunk:

        chunks.append(" ".join(current_chunk))

    return chunks


def save_chunks(chunks, output_file):

    output_file.parent.mkdir(parents=True, exist_ok=True)

    chunk_data = []

    for index, chunk in enumerate(chunks):

        chunk_data.append({
            "chunk_id": index,
            "chunk_index": index,
            "word_count": len(chunk.split()),
            "text": chunk
        })

    with open(output_file, "w", encoding="utf-8") as file:

        json.dump(
            chunk_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Chunks saved to: {output_file}")


if __name__ == "__main__":

    # Read cleaned text
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        text = file.read()

    print("Total words:", len(text.split()))

    # Split into paragraphs
    paragraphs = split_into_paragraphs(text)

    print("Paragraphs found:", len(paragraphs))

    # Create chunks
    chunks = create_chunks(
        paragraphs,
        max_words=400,
        overlap_words=80
    )

    print("Chunks created:", len(chunks))

    # Save chunks
    save_chunks(chunks, OUTPUT_FILE)

    # Show first chunk
    if chunks:

        print("\n===== FIRST CHUNK =====")
        print(chunks[0])
        print("\n===== END FIRST CHUNK =====")