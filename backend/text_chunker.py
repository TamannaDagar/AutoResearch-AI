from pathlib import Path
import json


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "papers"
    / "text"
    / "test_paper_cleaned.txt"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "papers"
    / "chunks"
    / "test_paper_chunks.json"
)

METADATA_FILE = (
    BASE_DIR
    / "data"
    / "papers"
    / "cleaned_papers.json"
)


# --------------------------------------------------
# Section detection
# --------------------------------------------------

SECTION_HEADINGS = {
    "ABSTRACT",
    "INTRODUCTION",
    "A SYSTEMS VIEW OF GENERATIVE AI IN EDUCATION",
    "BACKGROUND",
    "RELATED WORK",
    "LITERATURE REVIEW",
    "METHODOLOGY",
    "METHOD",
    "METHODS",
    "MATERIALS AND METHODS",
    "RESULTS",
    "DISCUSSION",
    "CONCLUSION",
    "CONCLUSIONS",
    "LIMITATIONS",
    "FUTURE WORK",
    "REFERENCES",
    "ACKNOWLEDGEMENTS",
    "ACKNOWLEDGMENTS",
}


def is_section_heading(line):
    """
    Check whether a line represents a research-paper section.
    """

    normalized = line.strip().upper()

    return normalized in SECTION_HEADINGS


# --------------------------------------------------
# Split text into sections
# --------------------------------------------------

def split_into_sections(text):
    """
    Divide the cleaned paper into logical sections.

    Returns:
        [
            {
                "section": "ABSTRACT",
                "text": "..."
            },
            {
                "section": "INTRODUCTION",
                "text": "..."
            }
        ]
    """

    lines = text.splitlines()

    sections = []

    current_section = "UNKNOWN"
    current_lines = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if is_section_heading(line):

            # Save previous section.
            if current_lines:

                section_text = " ".join(current_lines).strip()

                if section_text:
                    sections.append({
                        "section": current_section,
                        "text": section_text
                    })

            current_section = line.upper()
            current_lines = []

        else:
            current_lines.append(line)

    # Save final section.
    if current_lines:

        section_text = " ".join(current_lines).strip()

        if section_text:
            sections.append({
                "section": current_section,
                "text": section_text
            })

    return sections


# --------------------------------------------------
# Create chunks
# --------------------------------------------------

def create_chunks(
    sections,
    paper_metadata,
    max_words=400,
    overlap_words=80
):
    """
    Create chunks within each section.

    Chunks do not cross section boundaries.

    Each chunk also contains metadata
    identifying the research paper.
    """

    chunks = []

    for section_data in sections:

        section_name = section_data["section"]
        section_text = section_data["text"]

        words = section_text.split()

        start = 0

        while start < len(words):

            end = min(
                start + max_words,
                len(words)
            )

            chunk_words = words[start:end]

            chunk_text = " ".join(chunk_words)

            chunks.append({
                # Paper metadata
                "paper_id": paper_metadata["openalex_id"],
                "title": paper_metadata["title"],
                "year": paper_metadata["year"],
                "doi": paper_metadata["doi"],

                # Chunk metadata
                "chunk_id": len(chunks),
                "chunk_index": len(chunks),
                "section": section_name,
                "word_count": len(chunk_words),

                # Actual chunk text
                "text": chunk_text
            })

            # Stop if this is the final chunk.
            if end >= len(words):
                break

            # Move forward while keeping overlap.
            start = end - overlap_words

    return chunks


# --------------------------------------------------
# Save chunks
# --------------------------------------------------

def save_chunks(chunks, output_file):

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunks,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Chunks saved to: {output_file}"
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    # ----------------------------------------------
    # Step 1: Read paper metadata
    # ----------------------------------------------

    with open(
        METADATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        papers = json.load(file)

    # For the current test paper, find its metadata.
    paper_metadata = next(
        paper
        for paper in papers
        if paper["title"]
        == "Towards social generative AI for education: theory, practices and ethics"
    )

    print(
        "\nPaper:",
        paper_metadata["title"]
    )

    print(
        "Year:",
        paper_metadata["year"]
    )

    print(
        "DOI:",
        paper_metadata["doi"]
    )

    print(
        "OpenAlex ID:",
        paper_metadata["openalex_id"]
    )

    # ----------------------------------------------
    # Step 2: Read cleaned text
    # ----------------------------------------------

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    print(
        "\nTotal words:",
        len(text.split())
    )

    # ----------------------------------------------
    # Step 3: Detect sections
    # ----------------------------------------------

    sections = split_into_sections(text)

    print(
        "Sections found:",
        len(sections)
    )

    print("\nDetected sections:")

    for section in sections:

        print(
            f"- {section['section']}: "
            f"{len(section['text'].split())} words"
        )

    # ----------------------------------------------
    # Step 4: Create chunks
    # ----------------------------------------------

    chunks = create_chunks(
        sections,
        paper_metadata,
        max_words=400,
        overlap_words=80
    )

    print(
        "\nChunks created:",
        len(chunks)
    )

    # ----------------------------------------------
    # Step 5: Save chunks
    # ----------------------------------------------

    save_chunks(
        chunks,
        OUTPUT_FILE
    )

    # ----------------------------------------------
    # Step 6: Show first chunk
    # ----------------------------------------------

    if chunks:

        print(
            "\n===== FIRST CHUNK ====="
        )

        print(
            "Paper ID:",
            chunks[0]["paper_id"]
        )

        print(
            "Title:",
            chunks[0]["title"]
        )

        print(
            "Year:",
            chunks[0]["year"]
        )

        print(
            "DOI:",
            chunks[0]["doi"]
        )

        print(
            "Chunk ID:",
            chunks[0]["chunk_id"]
        )

        print(
            "Section:",
            chunks[0]["section"]
        )

        print(
            "Word count:",
            chunks[0]["word_count"]
        )

        print(
            "\nText:\n"
        )

        print(
            chunks[0]["text"]
        )

        print(
            "\n===== END FIRST CHUNK ====="
        )