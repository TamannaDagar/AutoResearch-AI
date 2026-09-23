from pathlib import Path
import json
import re


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
# Known academic section headings
# --------------------------------------------------

SECTION_HEADINGS = {
    "ABSTRACT",
    "INTRODUCTION",
    "BACKGROUND",
    "RELATED WORK",
    "LITERATURE REVIEW",
    "METHODOLOGY",
    "METHODOLOGICAL APPROACH",
    "METHOD",
    "METHODS",
    "MATERIALS AND METHODS",
    "RESULTS",
    "FINDINGS",
    "DISCUSSION",
    "DISCUSSION AND IMPLICATIONS",
    "CONCLUSION",
    "CONCLUSIONS",
    "LIMITATIONS",
    "FUTURE WORK",
    "IMPLICATIONS",
    "THEORETICAL IMPLICATIONS",
    "PRACTICAL IMPLICATIONS",
    "RECOMMENDATIONS",
    "ACKNOWLEDGEMENTS",
    "ACKNOWLEDGMENTS",
    "REFERENCES",
}


# --------------------------------------------------
# Section heading detection
# --------------------------------------------------

def is_section_heading(line):

    normalized = " ".join(line.strip().split())

    if not normalized:
        return False

    upper_line = normalized.upper()

    # Known academic heading
    if upper_line in SECTION_HEADINGS:
        return True

    # Numbered heading
    # Example: 1 Introduction
    # Example: 2.1 Methodology
    numbered_heading = re.match(
        r"^\d+(?:\.\d+)*\.?\s+[A-Za-z][A-Za-z\s&:-]{1,80}$",
        normalized
    )

    if numbered_heading:
        return True

    # Roman numeral heading
    # Example: I. Introduction
    roman_heading = re.match(
        r"^[IVXLC]+\.?\s+[A-Za-z][A-Za-z\s&:-]{1,80}$",
        normalized,
        re.IGNORECASE
    )

    if roman_heading:
        return True

    # Short uppercase heading
    if (
        normalized.isupper()
        and len(normalized.split()) <= 12
        and len(normalized) <= 100
    ):
        return True

    return False


# --------------------------------------------------
# Normalize section name
# --------------------------------------------------

def normalize_section_name(line):

    return " ".join(line.strip().split())


# --------------------------------------------------
# Parse sections
# --------------------------------------------------

def parse_sections(cleaned_text):

    sections = []

    current_section = "Unknown"
    current_text = []

    for line in cleaned_text.splitlines():

        line = line.strip()

        if not line:
            continue

        # ------------------------------------------
        # Section heading found
        # ------------------------------------------

        if is_section_heading(line):

            # Save previous section
            if current_text:

                section_text = " ".join(
                    current_text
                ).strip()

                if section_text:

                    sections.append({
                        "section": current_section,
                        "text": section_text
                    })

            # Start new section
            current_section = normalize_section_name(
                line
            )

            current_text = []

        else:

            current_text.append(line)

    # ------------------------------------------
    # Save final section
    # ------------------------------------------

    if current_text:

        section_text = " ".join(
            current_text
        ).strip()

        if section_text:

            sections.append({
                "section": current_section,
                "text": section_text
            })

    return sections


# --------------------------------------------------
# Backward-compatible function
# --------------------------------------------------

def split_into_sections(text):

    return parse_sections(text)


# --------------------------------------------------
# Create chunks
# --------------------------------------------------

def create_chunks(
    sections,
    paper_metadata,
    max_words=400,
    overlap_words=80
):

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

            chunk_text = " ".join(
                chunk_words
            )

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

                # Chunk text
                "text": chunk_text
            })

            # Final chunk
            if end >= len(words):
                break

            # Maintain overlap
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
# Main test
# --------------------------------------------------

if __name__ == "__main__":

    with open(
        METADATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        papers = json.load(file)

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

    sections = parse_sections(text)

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

    save_chunks(
        chunks,
        OUTPUT_FILE
    )