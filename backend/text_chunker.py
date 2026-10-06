
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

# Map heading variants to consistent section names.
HEADING_ALIASES = {
    "ABSTRACT": "Abstract",
    "INTRODUCTION": "Introduction",
    "BACKGROUND": "Background",
    "RELATED WORK": "Related Work",
    "LITERATURE REVIEW": "Literature Review",
    "METHODOLOGY": "Methodology",
    "METHODOLOGICAL APPROACH": "Methodology",
    "METHOD": "Methods",
    "METHODS": "Methods",
    "MATERIALS AND METHODS": "Methods",
    "RESEARCH DESIGN": "Methods",
    "DATA AND METHODS": "Methods",
    "RESULT": "Results",
    "RESULTS": "Results",
    "FINDINGS": "Findings",
    "DISCUSSION": "Discussion",
    "DISCUSSION AND IMPLICATIONS": "Discussion",
    "CONCLUSION": "Conclusion",
    "CONCLUSIONS": "Conclusion",
    "CONCLUDING REMARKS": "Conclusion",
    "LIMITATION": "Limitations",
    "LIMITATIONS": "Limitations",
    "FUTURE WORK": "Future Work",
    "FUTURE DIRECTIONS": "Future Work",
    "IMPLICATIONS": "Implications",
    "THEORETICAL IMPLICATIONS": "Implications",
    "PRACTICAL IMPLICATIONS": "Implications",
    "RECOMMENDATIONS": "Recommendations",
    "ACKNOWLEDGEMENTS": "Acknowledgements",
    "ACKNOWLEDGMENTS": "Acknowledgements",
    "REFERENCES": "References",
    "BIBLIOGRAPHY": "References",
    "WORKS CITED": "References",
}


REFERENCE_HEADINGS = {
    "REFERENCES",
    "BIBLIOGRAPHY",
    "WORKS CITED",
}


# --------------------------------------------------
# Heading normalization
# --------------------------------------------------

def clean_heading_text(line):
    """
    Normalize a possible heading by removing numbering
    and unnecessary whitespace.

    Examples:
    1 Introduction -> INTRODUCTION
    2.1 Methodology -> METHODOLOGY
    III. Results -> RESULTS
    """
    normalized = " ".join(line.strip().split())

    # Remove Arabic section numbers.
    normalized = re.sub(
        r"^\d+(?:\.\d+)*\.?\s*",
        "",
        normalized
    )

    # Remove Roman numeral prefixes.
    normalized = re.sub(
        r"^[IVXLC]+\.?\s+",
        "",
        normalized,
        flags=re.IGNORECASE
    )

    # Remove trailing punctuation.
    normalized = normalized.strip(" .:-")

    return normalized.upper()


def get_section_name(line):
    """
    Return a canonical section name if the line is a
    recognized heading. Otherwise return None.
    """
    normalized = clean_heading_text(line)

    if normalized in HEADING_ALIASES:
        return HEADING_ALIASES[normalized]

    return None


def is_section_heading(line):
    """
    Check whether a line is a recognized academic heading.
    """
    return get_section_name(line) is not None


# --------------------------------------------------
# Reference detection
# --------------------------------------------------

def is_reference_heading(line):
    """
    Identify bibliography headings so references are
    never included as research-content chunks.
    """
    normalized = clean_heading_text(line)
    return normalized in REFERENCE_HEADINGS


# --------------------------------------------------
# Parse sections
# --------------------------------------------------

def parse_sections(cleaned_text):
    """
    Split cleaned paper text into recognized sections.

    Text before the first recognized heading is ignored
    to avoid title-page and front-matter chunks.

    References and bibliography sections are excluded.
    """
    sections = []
    current_section = None
    current_text = []
    references_found = False

    def save_current_section():
        """
        Save the current section if it contains text.
        """
        nonlocal current_text, current_section

        section_text = " ".join(current_text).strip()

        if current_section and section_text:
            sections.append({
                "section": current_section,
                "text": section_text
            })

        current_text = []

    for line in cleaned_text.splitlines():
        line = line.strip()

        if not line:
            continue

        # Stop processing when references begin.
        if is_reference_heading(line):
            save_current_section()
            references_found = True
            print("References section detected. Stopping section parsing.")
            break

        # Recognized academic heading.
        section_name = get_section_name(line)

        if section_name:
            save_current_section()
            current_section = section_name
            continue

        # Ignore text before the first recognized heading.
        if current_section is None:
            continue

        current_text.append(line)

    # Save the final section if references were not reached.
    if not references_found:
        save_current_section()

    # If no recognized headings were found, retain the
    # document body under a neutral section name.
    if not sections:
        body_lines = []
        for line in cleaned_text.splitlines():
            line = line.strip()

            if not line:
                continue

            if is_reference_heading(line):
                break

            body_lines.append(line)

        body_text = " ".join(body_lines).strip()

        if body_text:
            sections.append({
                "section": "Content",
                "text": body_text
            })

    return sections


# --------------------------------------------------
# Backward-compatible function
# --------------------------------------------------

def split_into_sections(text):
    """
    Backward-compatible alias for parse_sections().
    """
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
    """
    Split each section into overlapping word chunks.

    Each chunk preserves paper metadata and its section.
    """
    if max_words <= 0:
        raise ValueError("max_words must be greater than zero.")

    if overlap_words < 0:
        raise ValueError("overlap_words cannot be negative.")

    if overlap_words >= max_words:
        raise ValueError(
            "overlap_words must be smaller than max_words."
        )

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

                # Chunk content
                "text": chunk_text
            })

            # Stop after the final chunk.
            if end >= len(words):
                break

            # Move forward while retaining overlap.
            start = end - overlap_words

    return chunks


# --------------------------------------------------
# Save chunks
# --------------------------------------------------

def save_chunks(chunks, output_file):
    """
    Save chunks to a JSON file.
    """
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

    print(f"Chunks saved to: {output_file}")


# --------------------------------------------------
# Main test
# --------------------------------------------------

if __name__ == "__main__":

    # Load paper metadata.
    with open(
        METADATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        papers = json.load(file)

    target_title = (
        "Towards social generative AI for education: "
        "theory, practices and ethics"
    )

    paper_metadata = next(
        (
            paper
            for paper in papers
            if paper["title"] == target_title
        ),
        None
    )

    if paper_metadata is None:
        raise ValueError(
            f"Paper not found in metadata: {target_title}"
        )

    print("\nPaper:", paper_metadata["title"])
    print("Year:", paper_metadata["year"])
    print("DOI:", paper_metadata["doi"])
    print("OpenAlex ID:", paper_metadata["openalex_id"])

    # Read cleaned text.
    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        text = file.read()

    print("\nTotal words:", len(text.split()))

    # Parse sections.
    sections = parse_sections(text)

    print("\nSections found:", len(sections))
    print("\nDetected sections:")

    for section in sections:
        print(
            f"- {section['section']}: "
            f"{len(section['text'].split())} words"
        )

    # Create chunks.
    chunks = create_chunks(
        sections,
        paper_metadata,
        max_words=400,
        overlap_words=80
    )

    print("\nChunks created:", len(chunks))

    # Save chunks.
    save_chunks(
        chunks,
        OUTPUT_FILE
    )

    print("\n===== CHUNK PREVIEW =====")

    for chunk in chunks[:3]:
        print("\nSection:", chunk["section"])
        print("Word count:", chunk["word_count"])
        print("Text:", chunk["text"][:500])

    print("\n===== END PREVIEW =====")