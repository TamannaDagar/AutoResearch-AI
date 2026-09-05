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
        paper= {
            "title": work.get("title"),
            "year": work.get("publication_year"),
            "doi": work.get("doi"),
            "cited_by_count": work.get("cited_by_count"),
            "openalex_id": work.get("id")
        }

        papers.append(paper)

    return papers
