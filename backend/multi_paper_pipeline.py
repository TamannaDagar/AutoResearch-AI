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

        title = paper.get("title", "unknown_paper")
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

        # Avoid downloading the same paper again
        if output_path.exists():
            print("PDF already exists.")
            downloaded_papers.append({
                "paper": paper,
                "pdf_path": output_path
            })
            continue

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


def main():

    print("\n========================================")
    print("       MULTI-PAPER INGESTION")
    print("========================================")

    papers = load_papers()

    print("\nTotal papers in metadata:", len(papers))

    available_papers = get_available_papers(papers)

    downloaded_papers = download_available_papers(
        available_papers
    )

    print("\n========================================")
    print("Downloaded papers:", len(downloaded_papers))
    print("========================================")

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

    print("\n========================================")


if __name__ == "__main__":
    main()