
import re


def remove_front_matter(text):
    """
    Remove publisher/journal information appearing before
    the actual research article.
    """
    lines = text.splitlines()

    for i, line in enumerate(lines):
        if re.match(r"^\s*abstract\s*$", line, re.IGNORECASE):
            print(f"Article start detected at line: {i + 1}")
            return "\n".join(lines[i:])

    print("Warning: Could not detect article start. Keeping full text.")
    return text


def remove_references_section(text):
    """
    Remove references, bibliography, and works-cited sections.
    """
    lines = text.splitlines()

    reference_heading = re.compile(
        r"^\s*(?:\d+(?:\.\d+)*\.?\s*)?"
        r"(?:references|bibliography|works cited)"
        r"(?:\s+and\s+notes)?\s*$",
        re.IGNORECASE
    )

    for i, line in enumerate(lines):
        if reference_heading.match(line):
            print(f"References section detected at line: {i + 1}")
            return "\n".join(lines[:i]).rstrip()

    print("Warning: References section not detected.")
    return text


def remove_publisher_blocks(text):
    """
    Remove publisher/footer content.

    Publisher-specific removal rules should be added only
    after checking extracted text to avoid deleting research.
    """
    return text


def remove_article_metadata(text):
    """
    Remove article history and keyword metadata without
    deleting the main research content.
    """

    # Remove ARTICLE HISTORY block only when a clear
    # following section marker is present.
    text = re.sub(
        r"(?is)\bARTICLE\s+HISTORY\b.*?"
        r"(?=\bKEYWORDS\b|\bABSTRACT\b|\bINTRODUCTION\b)",
        "",
        text,
        count=1
    )

    # Remove KEYWORDS block only when a clear section
    # heading follows it.
    text = re.sub(
        r"(?is)\bKEYWORDS?\b.*?"
        r"(?=\bABSTRACT\b|\bINTRODUCTION\b)",
        "",
        text,
        count=1
    )

    # Normalize repeated spaces and tabs.
    text = re.sub(r"[ \t]{2,}", " ", text)

    return text

def clean_soft_hyphens(text):
    """
    Fix invisible soft hyphens and words split across
    PDF line breaks.
    """

    # Remove Unicode soft hyphens.
    text = text.replace("\u00ad", "")

    # Join words split at a line break with a hyphen.
    # Example: genera-\ntive -> generative
    text = re.sub(
        r"-[ \t]*\n[ \t]*(?=\w)",
        "",
        text
    )

    return text


def fix_known_pdf_word_artifacts(text):
    """
    Repair known words split by unwanted spaces
    during PDF text extraction.
    """

    replacements = {
        r"\bexplora\s+tion\b": "exploration",
        r"\blan\s+guage\b": "language",
        r"\bhuman-AIsystem\b": "human-AI system",
        r"\btolearners\b": "to learners",
        r"\bTheOpen University\b": "The Open University",
        r"\bdiffer\s+ences\b": "differences",
        r"\bresponsi\s+bility\b": "responsibility",
        r"\bnarrowlydefined\b": "narrowly-defined",
        r"\bconversa\s+tions\b": "conversations",
        r"\bfunda\s+mental\b": "fundamental",
        r"\blearners,guides\b": "learners, guides",
    }

    for pattern, replacement in replacements.items():
        text = re.sub(
            pattern,
            replacement,
            text,
            flags=re.IGNORECASE
        )

    # Repair a few common missing-space artifacts.
    text = re.sub(
        r"\bhuman-AI(?=system\b)",
        "human-AI ",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\b(learners),(guides)\b",
        r"\1, \2",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\b(nurturing)(and)\b",
        r"\1 \2",
        text,
        flags=re.IGNORECASE
    )

    return text


def is_section_heading(line):
    """
    Detect common research-paper section headings,
    including numbered headings.
    """

    heading_patterns = [
        r"abstract",
        r"introduction",
        r"a systems view of generative AI in education",
        r"background",
        r"related work",
        r"literature review",
        r"methodology",
        r"methods?",
        r"materials and methods",
        r"results?",
        r"discussion",
        r"conclusions?",
        r"limitations?",
        r"future work",
        r"references",
        r"bibliography",
        r"works cited",
        r"acknowledgements?",
        r"acknowledgments?",
    ]

    cleaned_line = line.strip()

    # Remove leading section numbers such as 2.1 or 3.
    cleaned_line = re.sub(
        r"^\d+(?:\.\d+)*\.?\s*",
        "",
        cleaned_line
    )

    # Remove trailing punctuation sometimes attached to headings.
    cleaned_line = cleaned_line.rstrip(" .:")

    for pattern in heading_patterns:
        if re.fullmatch(pattern, cleaned_line, re.IGNORECASE):
            return True

    return False


def structure_text(text):
    """
    Preserve section headings while joining ordinary
    PDF line breaks into readable paragraphs.
    """

    headings = [
        "ABSTRACT",
        "Introduction",
        "A systems view of generative AI in education",
        "Background",
        "Related Work",
        "Literature Review",
        "Methodology",
        "Methods",
        "Materials and Methods",
        "Results",
        "Discussion",
        "Conclusion",
        "Conclusions",
        "Limitations",
        "Future Work",
        "References",
        "Bibliography",
        "Works Cited",
        "Acknowledgements",
        "Acknowledgments",
    ]

    # Put recognized headings on separate lines when
    # surrounded by whitespace.
    for heading in headings:
        pattern = (
            r"\s+"
            + re.escape(heading)
            + r"\s+"
        )

        replacement = "\n\n" + heading + "\n\n"

        text = re.sub(
            pattern,
            replacement,
            text,
            flags=re.IGNORECASE
        )

    lines = text.splitlines()
    blocks = []
    current_block = []

    for line in lines:
        line = line.strip()

        # An empty line ends the current paragraph.
        if not line:
            if current_block:
                blocks.append(" ".join(current_block))
                current_block = []
            continue

        # Preserve section headings as separate blocks.
        if is_section_heading(line):
            if current_block:
                blocks.append(" ".join(current_block))
                current_block = []

            blocks.append(line)
            continue

        current_block.append(line)

    # Add any remaining paragraph.
    if current_block:
        blocks.append(" ".join(current_block))

    cleaned_blocks = []

    for block in blocks:
        # Normalize whitespace.
        block = re.sub(r"\s+", " ", block)

        # Remove spaces before punctuation.
        block = re.sub(
            r"\s+([,.!?;:])",
            r"\1",
            block
        )

        block = block.strip()

        if block:
            cleaned_blocks.append(block)

    return "\n\n".join(cleaned_blocks)


def clean_text(text):
    """
    Main text-cleaning pipeline.
    """

    print("Original characters:", len(text))

    # STEP 1: Remove front matter.
    text = remove_front_matter(text)
    print("Characters after front matter removal:", len(text))

    # STEP 2: Remove references and bibliography.
    text = remove_references_section(text)
    print("Characters after references removal:", len(text))

    # STEP 3: Remove publisher-specific blocks.
    text = remove_publisher_blocks(text)
    print("Characters after publisher cleanup:", len(text))

    # STEP 4: Remove article metadata.
    text = remove_article_metadata(text)
    print("Characters after metadata cleanup:", len(text))

    # STEP 5: Fix PDF extraction artifacts.
    text = clean_soft_hyphens(text)

    # STEP 6: Repair known broken words.
    text = fix_known_pdf_word_artifacts(text)

    # STEP 7: Preserve research-paper structure.
    text = structure_text(text)

    print("Cleaned characters:", len(text))

    return text


def save_cleaned_text(text, output_file):
    """
    Save cleaned text to a UTF-8 text file.
    """

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(text)

    print(f"Cleaned text saved to: {output_file}")


if __name__ == "__main__":

    # Input and output paths.
    input_file = "data/papers/text/test_paper.txt"
    output_file = "data/papers/text/test_paper_cleaned.txt"

    # Read extracted text.
    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as file:
        raw_text = file.read()

    # Clean text.
    cleaned_text = clean_text(raw_text)

    # Save cleaned text.
    save_cleaned_text(
        cleaned_text,
        output_file
    )

    # Display a preview.
    print("\n===== CLEANED TEXT PREVIEW =====")
    print(cleaned_text[:3000])
    print("\n===== END PREVIEW =====")