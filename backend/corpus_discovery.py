from pathlib import Path
import json

from paper_search import search_papers


BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "papers"
    / "search_results_expanded.json"
)


def discover_papers(topic, per_page=30):

    print("\n========================================")
    print("        EXPANDED PAPER DISCOVERY")
    print("========================================")

    print("\nResearch Topic:")
    print(topic)

    print("\nSearching OpenAlex...")

    papers = search_papers(
        topic,
        per_page=per_page
    )

    print("\nPapers retrieved:", len(papers))

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

    print(
        "\nSearch results saved to:"
    )

    print(OUTPUT_FILE)

    print("\n========================================")
    print("          PAPER SUMMARY")
    print("========================================")

    for index, paper in enumerate(
        papers,
        start=1
    ):

        print(
            f"\n[{index}] "
            f"{paper.get('title')}"
        )

        print(
            "Year:",
            paper.get("year")
        )

        print(
            "Open Access:",
            paper.get("is_oa")
        )

        print(
            "PDF URL:",
            paper.get("pdf_url")
        )

    print("\n========================================")

    return papers


if __name__ == "__main__":

    topic = (
        "generative AI in education"
    )

    discover_papers(
        topic,
        per_page=30
    )