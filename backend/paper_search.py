import requests

# create function
def search_papers(topic, per_page=10):
    url= "https://api.openalex.org/works"

# parametrs that will be show - topic and no. of page
    params= {
        "search": topic,
        "per_page": per_page
    }

    response= requests.get(url, params=params)

    if response.status_code != 200:
        print("Error While Seraching Paper")
        return[]

    data=response.json()
    papers= []

    for work in data['results']:

        #----------------------
        # Get Open Access Information
        #----------------------
        print("\nTITLE:", work.get("title"))
        open_access= work.get("open_access", {})

        best_oa_location= work.get("best_oa_location")

        print("OPEN ACCESS:", open_access)
        print("BEST OA LOCATION:", best_oa_location)

        pdf_url= None

        if best_oa_location:
            pdf_url = best_oa_location.get("pdf_url")

        if not pdf_url:
            pdf_url= open_access.get("oa_url")

        #------------------------------
        # Create Paper Object
        #------------------------------

        paper= {
            "title": work.get("title"),
            "year": work.get("publication_year"),
            "doi": work.get("doi"),
            "cited_by_count": work.get("cited_by_count"),
            "openalex_id": work.get("id"),
            "is_oa": open_access.get("is_oa", False),
            'pdf_url': pdf_url
        }

        papers.append(paper)

    return papers
