#import fitz
import pymupdf
import os


def extract_text_from_pdf(pdf_path):
    """
    Extract Text from all the pages of the pdf
    
    Returns:
    str: Combined text from the pdf"""

    if not os.path.exists(pdf_path):
        print(f'PDF not found: {pdf_path}')
        return ""

    try:
        document= pymupdf.open(pdf_path)

        extracted_text= []

        for page_numebr, page in enumerate(document, start=1):

            text= page.get_text("text")

            if text.strip():
                extracted_text.append(text)

            else:
                print(f'Warning: No text found on page {page_numebr}')
        document.close()

        return"\n".join(extracted_text)

    except Exception as e:
        print("Error extracting PDF:", e)
        return ""

def save_extracted_text(text, output_file):
    """
    Save Extracted text to a .txt file."""

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding='utf-8') as file:
        file.write(text)

        print(f"Extracted text saved to: {output_file}")

if __name__ == "__main__":
    pdf_path= "data/papers/pdfs/test_paper.pdf"
    output_file= "data/papers/text/test_paper.txt"

    text= extract_text_from_pdf(pdf_path)

    if text:
        save_extracted_text(text, output_file)

        print("\n Text Extraction successful!")
        print("Characters extracted:", len(text))

        print("\n===== EXTRACTED TEXT PREVIEW =====")
        print(repr(text[:500]))
        print("===== END PREVIEW =====")

    else:
        print("No text could be extracted.")
        