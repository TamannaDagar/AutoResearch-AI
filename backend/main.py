from paper_search import search_papers
import json

topic= "Generative AI in Education"

papers= search_papers(topic, 10)

with open ('data/papers/search_results.json', 'w', encoding='utf-8' ) as file:
    json.dump(papers, file, indent=4, ensure_ascii=False)

print(f"Found {len(papers)} papers")
print("Result saved successfully!")


for paper in papers:
    print("\n Title:", paper['title'] )
    print('Year:', paper['year'])
    print('DOI:', paper['doi'])
    print("Citations:", paper['cited_by_count'])