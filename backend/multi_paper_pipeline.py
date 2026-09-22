from pathlib import Path
import json

from paper_pipeline import process_one_paper
from pdf_downloader import download_pdf


BASE_DIR = Path(__file__).resolve().parent.parent

METADATA_FILE = (
    BASE_DIR
    / "data"
    / "papers"
    / "cleaned_papers.json"
)

PDF_DIRECTORY = (
    BASE_DIR
    / "data"
    / "papers"
    / "pdfs"
)


def load_papers():
    with open(METADATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_available_papers(papers):
    """
    Select papers that have:
    1. Open-access status
    2. A direct PDF URL
    """

    available = []

    for paper in papers:

        pdf_url = paper.get("pdf_url")
        is_oa = paper.get("is_oa")

        if is_oa and pdf_url:
            available.append(paper)

    return available


def download_available_papers(papers):

    downloaded_papers = []

    for index, paper in enumerate(papers, start=1):

        title = paper.get(
            "title",
            "unknown_paper"
        )

        pdf_url = paper.get("pdf_url")

        print("\n----------------------------------------")
        print(f"Paper {index}: {title}")

        if not pdf_url:
            print("No PDF URL. Skipping.")
            continue

        paper_id = paper.get("openalex_id")

        if not paper_id:
            print("No OpenAlex ID. Skipping.")
            continue

        output_path = (
            PDF_DIRECTORY
            / f"{paper_id.replace('/', '_')}.pdf"
        )

        # -------------------------------------
        # Check whether PDF already exists
        # -------------------------------------
        if output_path.exists():

            print("PDF already exists.")

            downloaded_papers.append({
                "paper": paper,
                "pdf_path": output_path
            })

            continue

        # -------------------------------------
        # Download PDF
        # -------------------------------------
        try:

            print("Downloading PDF...")

            download_pdf(
                pdf_url,
                output_path
            )

            print(
                "Downloaded:",
                output_path
            )

            downloaded_papers.append({
                "paper": paper,
                "pdf_path": output_path
            })

        except Exception as error:

            print(
                "Download failed:",
                error
            )

    return downloaded_papers


def process_downloaded_papers(downloaded_papers):

    """
    Process every successfully downloaded paper.

    Each paper goes through:

    PDF
    ↓
    Text extraction
    ↓
    Cleaning
    ↓
    Section parsing
    ↓
    Chunking
    ↓
    Embeddings
    ↓
    Qdrant
    """

    processed_papers = []

    for index, item in enumerate(
        downloaded_papers,
        start=1
    ):

        paper = item["paper"]
        pdf_path = item["pdf_path"]

        print("\n========================================")
        print(f"PROCESSING PAPER {index}")
        print("========================================")

        print("Title:", paper.get("title"))
        print("PDF:", pdf_path)

        try:

            result = process_one_paper(
                pdf_path,
                paper
            )

            processed_papers.append(result)

            print("\nPaper processed successfully.")

        except Exception as error:

            print("\nPaper processing failed:")
            print(error)

    return processed_papers


def main():

    print("\n========================================")
    print("       MULTI-PAPER INGESTION")
    print("========================================")

    # -------------------------------------
    # 1. Load metadata
    # -------------------------------------
    papers = load_papers()

    print(
        "\nTotal papers in metadata:",
        len(papers)
    )

    # -------------------------------------
    # 2. Find papers with direct PDF URLs
    # -------------------------------------
    available_papers = get_available_papers(
        papers
    )

    print(
        "Papers with accessible PDF:",
        len(available_papers)
    )

    print("\nAvailable papers:")

    for index, paper in enumerate(
        available_papers,
        start=1
    ):

        print(
            f"{index}. "
            f"{paper.get('title')}"
        )

    # -------------------------------------
    # 3. Download PDFs
    # -------------------------------------
    downloaded_papers = download_available_papers(
        available_papers
    )

    print("\n========================================")
    print(
        "Downloaded papers:",
        len(downloaded_papers)
    )
    print("========================================")

    # -------------------------------------
    # 4. Process downloaded PDFs
    # -------------------------------------
    processed_papers = process_downloaded_papers(
        downloaded_papers
    )

    # -------------------------------------
    # 5. Final summary
    # -------------------------------------
    print("\n========================================")
    print("       INGESTION SUMMARY")
    print("========================================")

    print(
        "Papers successfully processed:",
        len(processed_papers)
    )

    print("========================================")


if __name__ == "__main__":
    main()