import re


def clean_text(text):
    """
    Clean extracted PDF text while preserving paragraph structure.
    """

    # 1. Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # 2. Fix words broken by a hyphen at the end of a line
    # Example:
    # gener-
    # ative
    #
    # becomes:
    # generative
    text = re.sub(r"-\n(?=\w)", "", text)

    # 3. Remove spaces at the beginning/end of each line
    lines = [line.strip() for line in text.split("\n")]

    # 4. Remove completely empty lines temporarily
    # while remembering paragraph boundaries
    paragraphs = []
    current_paragraph = []

    for line in lines:

        if line:
            current_paragraph.append(line)

        else:
            if current_paragraph:
                paragraphs.append(" ".join(current_paragraph))
                current_paragraph = []

    # Add the final paragraph
    if current_paragraph:
        paragraphs.append(" ".join(current_paragraph))

    # 5. Clean multiple spaces inside paragraphs
    cleaned_paragraphs = []

    for paragraph in paragraphs:
        paragraph = re.sub(r"\s+", " ", paragraph)
        paragraph = re.sub(r"\s+([,.!?;:])", r"\1", paragraph)
        cleaned_paragraphs.append(paragraph.strip())

    # 6. Put paragraphs on separate lines
    cleaned_text = "\n\n".join(cleaned_paragraphs)

    return cleaned_text


def save_cleaned_text(text, output_file):

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(text)

    print(f"Cleaned text saved to: {output_file}")


if __name__ == "__main__":

    input_file = "data/papers/text/test_paper.txt"
    output_file = "data/papers/text/test_paper_cleaned.txt"

    # Read extracted text
    with open(input_file, "r", encoding="utf-8") as file:
        raw_text = file.read()

    print("Original characters:", len(raw_text))

    # Clean text
    cleaned_text = clean_text(raw_text)

    print("Cleaned characters:", len(cleaned_text))

    # Save cleaned text
    save_cleaned_text(cleaned_text, output_file)

    # Preview
    print("\n===== CLEANED TEXT PREVIEW =====")
    print(cleaned_text[:2000])
    print("\n===== END PREVIEW =====")