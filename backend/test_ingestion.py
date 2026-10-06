
import json
from pathlib import Path

from paper_pipeline import process_one_paper


BASE_DIR = Path(__file__).resolve().parent.parent
METADATA_FILE = BASE_DIR / "data" / "papers" / "cleaned_papers.json"
PDF_FILE = BASE_DIR / "data" / "papers" / "pdfs" / "test_paper.pdf"


def main():
    with open(METADATA_FILE, "r", encoding="utf-8") as file:
        papers = json.load(file)

    target_title = (
        "Towards social generative AI for education: "
        "theory, practices and ethics"
    )

    paper_metadata = next(
        (paper for paper in papers if paper["title"] == target_title),
        None,
    )

    if paper_metadata is None:
        raise ValueError(f"Paper not found: {target_title}")

    if not PDF_FILE.exists():
        raise FileNotFoundError(f"PDF not found: {PDF_FILE}")

    result = process_one_paper(PDF_FILE, paper_metadata)

    print("\nTest ingestion completed.")
    print("Paper:", result["paper"]["title"])
    print("Chunks:", len(result["chunks"]))


if __name__ == "__main__":
    main()