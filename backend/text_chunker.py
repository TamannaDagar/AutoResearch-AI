import requests


# -------------------------------------
# Find a direct PDF from OA locations
# -------------------------------------
def get_direct_pdf_url(work):
    """
    Search OpenAlex OA locations for a direct PDF URL.

    Priority:
    1. best_oa_location
    2. other locations

    We never use oa_url as a PDF URL because
    it may point to a landing page or DOI.
    """

    locations = work.get("locations", [])

    # -------------------------------------
    # First: best OA location
    # -------------------------------------

    best_location = work.get("best_oa_location")

    if best_location:

        pdf_url = best_location.get("pdf_url")

        if pdf_url:
            return pdf_url

    # -------------------------------------
    # Second: other OA locations
    # -------------------------------------

    for location in locations:

        if not location:
            continue

        pdf_url = location.get("pdf_url")

        if pdf_url:
            return pdf_url

    return None


# -------------------------------------
# Search OpenAlex
# -------------------------------------
def search_papers(topic, per_page=10):

    url = "https://api.openalex.org/works"

    params = {
        "search": topic,
        "per_page": per_page
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    if response.status_code != 200:

        print("Error While Searching Papers")
        print("Status Code:", response.status_code)

        return []

    data = response.json()

    papers = []

    for work in data["results"]:

        # -------------------------------------
        # Open access information
        # -------------------------------------

        open_access = work.get(
            "open_access",
            {}
        )

        # -------------------------------------
        # Find direct PDF
        # -------------------------------------

        pdf_url = get_direct_pdf_url(work)

        # -------------------------------------
        # Create paper object
        # -------------------------------------

        paper = {

            "title": work.get("title"),

            "year": work.get(
                "publication_year"
            ),

            "doi": work.get("doi"),

            "cited_by_count": work.get(
                "cited_by_count",
                0
            ),

            "openalex_id": work.get("id"),

            "is_oa": open_access.get(
                "is_oa",
                False
            ),

            "pdf_url": pdf_url
        }

        papers.append(paper)

    return papers