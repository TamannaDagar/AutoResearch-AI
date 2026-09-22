import requests


# -------------------------------------
# Search OpenAlex for research papers
# -------------------------------------
def search_papers(topic, per_page=10):

    url = "https://api.openalex.org/works"

    # Parameters
    params = {
        "search": topic,
        "per_page": per_page
    }

    response = requests.get(url, params=params, timeout=30)

    if response.status_code != 200:
        print("Error While Searching Papers")
        print("Status Code:", response.status_code)
        return []

    data = response.json()

    papers = []

    for work in data["results"]:

        # -------------------------------------
        # Get Open Access Information
        # -------------------------------------
        open_access = work.get("open_access", {})

        best_oa_location = work.get("best_oa_location")

        # -------------------------------------
        # Get Direct PDF URL
        # -------------------------------------
        pdf_url = None

        if best_oa_location:
            pdf_url = best_oa_location.get("pdf_url")

        # IMPORTANT:
        # Do NOT fall back to open_access["oa_url"].
        # oa_url may be a DOI or landing page,
        # not an actual PDF.
        
        # -------------------------------------
        # Create Paper Object
        # -------------------------------------
        paper = {
            "title": work.get("title"),
            "year": work.get("publication_year"),
            "doi": work.get("doi"),
            "cited_by_count": work.get("cited_by_count", 0),
            "openalex_id": work.get("id"),
            "is_oa": open_access.get("is_oa", False),
            "pdf_url": pdf_url
        }

        papers.append(paper)

    return papers