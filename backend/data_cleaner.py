import json


def get_pdf_url(paper):
    """
    Return a direct PDF URL if one is available.

    We intentionally do not use DOI or general OA landing-page URLs
    as PDF URLs because they may return HTML instead of a PDF.
    """

    pdf_url = paper.get("pdf_url")

    if pdf_url:
        return pdf_url

    return None


def clean_papers(input_file, output_file):

    # Read raw paper data
    with open(input_file, "r", encoding="utf-8") as file:
        papers = json.load(file)

    cleaned_papers = []
    seen_dois = set()

    for paper in papers:

        # -------------------------------------
        # Get fields
        # -------------------------------------
        title = paper.get("title")
        year = paper.get("year")
        doi = paper.get("doi")

        # -------------------------------------
        # 1. Remove papers without title
        # -------------------------------------
        if not title:
            continue

        # -------------------------------------
        # 2. Clean Title
        # -------------------------------------
        title = title.strip()

        # -------------------------------------
        # 3. Clean DOI
        # -------------------------------------
        if doi:
            doi = doi.strip().lower()

        # -------------------------------------
        # 4. Remove Duplicate DOI
        # -------------------------------------
        if doi:
            if doi in seen_dois:
                continue

            seen_dois.add(doi)

        # -------------------------------------
        # 5. Normalize Year
        # -------------------------------------
        if year:
            try:
                year = int(year)
            except (ValueError, TypeError):
                year = None

        # -------------------------------------
        # 6. Get direct PDF URL
        # -------------------------------------
        pdf_url = get_pdf_url(paper)

        # -------------------------------------
        # 7. Create Cleaned Paper
        # -------------------------------------
        cleaned_paper = {
            "title": title,
            "year": year,
            "doi": doi,
            "cited_by_count": paper.get("cited_by_count", 0),
            "openalex_id": paper.get("openalex_id"),
            "is_oa": paper.get("is_oa", False),
            "pdf_url": pdf_url
        }

        cleaned_papers.append(cleaned_paper)

    # -------------------------------------
    # 8. Save Cleaned Data
    # -------------------------------------
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            cleaned_papers,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Cleaning completed successfully!")
    print("Total cleaned papers:", len(cleaned_papers))

    return cleaned_papers