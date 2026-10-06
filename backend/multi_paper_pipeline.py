from pathlib import Path
import json

from paper_pipeline import process_one_paper
from pdf_downloader import download_pdf


BASE_DIR = Path(__file__).resolve().parent.parent

ACCESSIBLE_PAPERS_FILE = (
    BASE_DIR
    / "data"
    / "papers"
    / "accessible_papers.json"
)

PDF_DIRECTORY = (
    BASE_DIR
    / "data"
    / "papers"
    / "pdfs"
)


def load_accessible_papers():

    with open(
        ACCESSIBLE_PAPERS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def create_pdf_filename(paper):

    paper_id = paper.get(
        "openalex_id",
        "unknown_paper"
    )

    # Convert the OpenAlex URL into a safe filename.
    safe_id = (
        paper_id
        .replace("https://", "")
        .replace("http://", "")
        .replace("/", "_")
        .replace(":", "_")
    )

    return f"{safe_id}.pdf"


def download_accessible_papers(papers):

    downloaded_papers = []

    PDF_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    print("\n========================================")
    print("          DOWNLOADING PAPERS")
    print("========================================")

    for index, paper in enumerate(
        papers,
        start=1
    ):

        title = paper.get(
            "title",
            "Unknown paper"
        )

        pdf_url = paper.get(
            "pdf_url"
        )

        print("\n----------------------------------------")

        print(
            f"Paper {index}: {title}"
        )

        if not pdf_url:

            print(
                "No PDF URL. Skipping."
            )

            continue

        output_path = (
            PDF_DIRECTORY
            / create_pdf_filename(paper)
        )

        print(
            "PDF URL:",
            pdf_url
        )

        print(
            "Output:",
            output_path
        )

        # Don't download again if the PDF already exists.
        if output_path.exists():

            print(
                "PDF already exists."
            )

            downloaded_papers.append(
                {
                    "paper": paper,
                    "pdf_path": output_path
                }
            )

            continue

        try:

            download_pdf(
                pdf_url,
                output_path
            )

            print(
                "Download successful."
            )

            downloaded_papers.append(
                {
                    "paper": paper,
                    "pdf_path": output_path
                }
            )

        except Exception as error:

            print(
                "Download failed:",
                error
            )

    return downloaded_papers


def process_downloaded_papers(
    downloaded_papers
):

    processed_papers = []

    print("\n========================================")
    print("          PROCESSING PAPERS")
    print("========================================")

    for index, item in enumerate(
        downloaded_papers,
        start=1
    ):

        paper = item["paper"]
        pdf_path = item["pdf_path"]

        print("\n========================================")
        print(
            f"PROCESSING PAPER {index}"
        )
        print("========================================")

        print(
            "Title:",
            paper.get("title")
        )

        print(
            "Year:",
            paper.get("year")
        )

        print(
            "DOI:",
            paper.get("doi")
        )

        print(
            "PDF:",
            pdf_path
        )

        try:

            result = process_one_paper(
                pdf_path,
                paper
            )

            processed_papers.append(
                result
            )

            print(
                "\nPaper processed successfully."
            )

        except Exception as error:

            print(
                "\nPaper processing failed:"
            )

            print(error)

    return processed_papers


def main():

    print("\n========================================")
    print("       MULTI-PAPER INGESTION")
    print("========================================")

    papers = load_accessible_papers()

    # Paper IDs belonging to the current research run.
    current_paper_ids = [
        paper["openalex_id"]
        for paper in papers
    ]

    print(
        "\nAccessible papers:",
        len(papers)
    )

    print("\nCurrent paper IDs:")

    for paper_id in current_paper_ids:

        print(
            paper_id
        )

    for index, paper in enumerate(
        papers,
        start=1
    ):

        print(
            f"{index}. {paper.get('title')}"
        )

    downloaded_papers = (
        download_accessible_papers(
            papers
        )
    )

    print("\n========================================")
    print("         DOWNLOAD SUMMARY")
    print("========================================")

    print(
        "Papers successfully downloaded:",
        len(downloaded_papers)
    )

    processed_papers = (
        process_downloaded_papers(
            downloaded_papers
        )
    )

    print("\n========================================")
    print("        INGESTION SUMMARY")
    print("========================================")

    print(
        "Papers successfully processed:",
        len(processed_papers)
    )

    print(
        "Qdrant collection:",
        "research_papers"
    )

    print("========================================")


if __name__ == "__main__":

    main()