from paper_search import search_papers
from data_cleaner import clean_papers
import json

topic= "Generative AI in Education"


#---------------------------
# Step 1. Search Papers
#---------------------------

papers= search_papers(topic, 10)

with open ('data/papers/search_results.json', 'w', encoding='utf-8' ) as file:
    json.dump(papers, file, indent=4, ensure_ascii=False)

print(f"Found {len(papers)} papers")
print(" Raw Result saved successfully!")

#---------------------------
# Step 2. Clean Papers
#---------------------------

cleaned_papers= clean_papers(
    "data/papers/search_results.json",
    "data/papers/cleaned_papers.json"
)
print(f"Cleaned Papers: {len(cleaned_papers)}")
print("Cleaned results saved Successfully!")

#-------------------------------
# Step 3. Display cleaned papers
#-------------------------------

for paper in cleaned_papers:
    print("\n Title:", paper['title'] )
    print('Year:', paper['year'])
    print('DOI:', paper['doi'])
    print("Citations:", paper['cited_by_count'])
    print("Open Access:", paper["is_oa"])
    print("PDF URL:", paper["pdf_url"])