import re


def remove_front_matter(text):
    """
    Remove publisher/journal information that appears
    before the actual research article.
    """

    lines = text.splitlines()

    article_start = None

    for i, line in enumerate(lines):
        if line.strip().upper() == "ABSTRACT":
            article_start = i
            break

    if article_start is not None:
        print(f"Article start detected at line: {article_start + 1}")
        return "\n".join(lines[article_start:])

    print("Warning: Could not detect article start. Keeping full text.")
    return text


def remove_publisher_blocks(text):
    """
    Remove obvious publisher/footer content that may appear
    inside the extracted article.
    """

    # Remove the publisher block that begins with the journal name.
    text = re.sub(
        r"(?is)"
        r"LEARNING:\s*RESEARCH\s*AND\s*PRACTICE"
        r".*?"
        r"with their consent\.",
        "",
        text,
        count=1
    )

    return text


def clean_soft_hyphens(text):
    """
    Fix invisible and line-break characters introduced
    during PDF text extraction.
    """

    # Remove Unicode soft-hyphen characters.
    text = text.replace("\u00ad", "")

    # Fix words split across a PDF line break.
    # Example:
    # gener-
    # ative
    # becomes:
    # generative
    text = re.sub(
        r"-\s*\n\s*(?=\w)",
        "",
        text
    )

    return text


def fix_known_pdf_word_artifacts(text):
    """
    Fix word fragments observed in the current PDF.

    PDF extraction can sometimes insert spaces into
    words even when no visible space exists in the PDF.
    """

    replacements = {
        "explora tion": "exploration",
        "lan guage": "language",
        "differ ences": "differences",
        "responsi bility": "responsibility",
        "narrowlydefined": "narrowly-defined",
    }

    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)

    return text


def is_section_heading(line):
    """
    Detect common research-paper section headings.
    """

    heading_patterns = [
        r"^ABSTRACT$",
        r"^Introduction$",
        r"^A systems view of generative AI in education$",
        r"^Background$",
        r"^Related Work$",
        r"^Literature Review$",
        r"^Methodology$",
        r"^Methods?$",
        r"^Materials and Methods$",
        r"^Results?$",
        r"^Discussion$",
        r"^Conclusion$",
        r"^Conclusions$",
        r"^Limitations?$",
        r"^Future Work$",
        r"^References$",
        r"^Acknowledgements?$",
        r"^Acknowledgments?$",
    ]

    for pattern in heading_patterns:
        if re.match(
            pattern,
            line.strip(),
            re.IGNORECASE
        ):
            return True

    return False


def structure_text(text):
    """
    Preserve important section headings while joining
    normal PDF line breaks.
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
        "Acknowledgements",
        "Acknowledgments",
    ]

    # Put headings on their own lines even when PDF extraction
    # placed them in the middle of a paragraph.
    for heading in headings:

        pattern = (
            r"\s+"
            + re.escape(heading)
            + r"\s+"
        )

        replacement = (
            "\n\n"
            + heading
            + "\n\n"
        )

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

        # Empty line = end of current block.
        if not line:

            if current_block:
                blocks.append(
                    " ".join(current_block)
                )

                current_block = []

            continue

        # If this line is a section heading,
        # keep it as a separate block.
        if is_section_heading(line):

            if current_block:
                blocks.append(
                    " ".join(current_block)
                )

                current_block = []

            blocks.append(line)

            continue

        current_block.append(line)

    # Add remaining text.
    if current_block:
        blocks.append(
            " ".join(current_block)
        )

    cleaned_blocks = []

    for block in blocks:

        # Remove excessive whitespace.
        block = re.sub(
            r"\s+",
            " ",
            block
        )

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

    print(
        "Original characters:",
        len(text)
    )

    # --------------------------------------------------
    # STEP 1: Remove publisher information before article
    # --------------------------------------------------

    text = remove_front_matter(text)

    print(
        "Characters after front matter removal:",
        len(text)
    )

    # --------------------------------------------------
    # STEP 2: Remove publisher/footer blocks
    # --------------------------------------------------

    text = remove_publisher_blocks(text)

    print(
        "Characters after publisher cleanup:",
        len(text)
    )

    # --------------------------------------------------
    # STEP 3: Fix PDF extraction artifacts
    # --------------------------------------------------

    text = clean_soft_hyphens(text)

    # --------------------------------------------------
    # STEP 4: Fix known word-splitting problems
    # --------------------------------------------------

    text = fix_known_pdf_word_artifacts(text)

    # --------------------------------------------------
    # STEP 5: Preserve research-paper structure
    # --------------------------------------------------

    text = structure_text(text)

    print(
        "Cleaned characters:",
        len(text)
    )

    return text


def save_cleaned_text(text, output_file):
    """
    Save cleaned text to a file.
    """

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(text)

    print(
        f"Cleaned text saved to: {output_file}"
    )


if __name__ == "__main__":

    # --------------------------------------------------
    # Input and output paths
    # --------------------------------------------------

    input_file = (
        "data/papers/text/test_paper.txt"
    )

    output_file = (
        "data/papers/text/test_paper_cleaned.txt"
    )

    # --------------------------------------------------
    # Read raw extracted text
    # --------------------------------------------------

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as file:

        raw_text = file.read()

    # --------------------------------------------------
    # Clean text
    # --------------------------------------------------

    cleaned_text = clean_text(
        raw_text
    )

    # --------------------------------------------------
    # Save cleaned text
    # --------------------------------------------------

    save_cleaned_text(
        cleaned_text,
        output_file
    )

    # --------------------------------------------------
    # Show preview
    # --------------------------------------------------

    print(
        "\n===== CLEANED TEXT PREVIEW ====="
    )

    print(
        cleaned_text[:3000]
    )

    print(
        "\n===== END PREVIEW ====="
    )