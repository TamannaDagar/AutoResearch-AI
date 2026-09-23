import json
from pathlib import Path

import requests


BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "papers"
    / "search_results_expanded.json"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "papers"
    / "accessible_papers.json"
)


def check_pdf_access(pdf_url):
    try:
        response = requests.get(
            pdf_url,
            timeout=30,
            stream=True
        )

        status_code = response.status_code
        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        is_pdf = (
            "application/pdf" in content_type
            or response.raw.read(4) == b"%PDF"
        )

        accessible = (
            status_code == 200
            and is_pdf
        )

        if accessible:
            reason = "Accessible PDF"
        else:
            reason = f"HTTP {status_code}"

        return {
            "accessible": accessible,
            "status_code": status_code,
            "content_type": content_type,
            "reason": reason
        }

    except Exception as error:
        return {
            "accessible": False,
            "status_code": None,
            "content_type": None,
            "reason": str(error)
        }


def load_papers():
    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def save_accessible_papers(papers):
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            papers,
            file,
            indent=4,
            ensure_ascii=False
        )


def main():

    print("\n========================================")
    print("          PDF ACCESS CHECK")
    print("========================================")

    papers = load_papers()

    accessible_papers = []

    direct_pdf_candidates = [
        paper
        for paper in papers
        if paper.get("pdf_url")
    ]

    print(
        "\nDirect PDF candidates:",
        len(direct_pdf_candidates)
    )

    for index, paper in enumerate(
        direct_pdf_candidates,
        start=1
    ):

        title = paper.get(
            "title",
            "Unknown paper"
        )

        pdf_url = paper.get("pdf_url")

        print("\n----------------------------------------")
        print(f"Paper {index}: {title}")

        result = check_pdf_access(pdf_url)

        print(
            "Status:",
            result["status_code"]
        )

        print(
            "Content-Type:",
            result["content_type"]
        )

        print(
            "Accessible:",
            result["accessible"]
        )

        print(
            "Reason:",
            result["reason"]
        )

        if result["accessible"]:

            accessible_papers.append(paper)

    print("\n========================================")
    print("             SUMMARY")
    print("========================================")

    print(
        "PDF candidates:",
        len(direct_pdf_candidates)
    )

    print(
        "Accessible PDFs:",
        len(accessible_papers)
    )

    print(
        "Inaccessible/invalid:",
        len(direct_pdf_candidates)
        - len(accessible_papers)
    )

    # Save verified accessible papers
    save_accessible_papers(accessible_papers)

    print("\n========================================")
    print("       ACCESSIBLE PAPERS SAVED")
    print("========================================")

    print(
        "Saved:",
        len(accessible_papers)
    )

    print(
        "Output file:",
        OUTPUT_FILE
    )

    print("\nAccessible papers:")

    for index, paper in enumerate(
        accessible_papers,
        start=1
    ):
        print(
            f"{index}. {paper.get('title')}"
        )

    print("\n========================================")


if __name__ == "__main__":
    main()