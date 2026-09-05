import json

def clean_papers(input_file, output_file):
    # Read raw paper data
    with open (input_file, 'r', encoding='utf-8') as file:
        papers=json.load(file)

        cleaned_papers = []
        seen_dois= set()

        for paper in papers:

            # Get fields
            title= paper.get("title")
            year = paper.get("year")
            doi= paper.get("doi")

            #-------------------------------------
            # 1. Remove papers without title
            #-------------------------------------
            if not title:
                continue

            #-------------------------------------
            # 2. Clean Title
            #-------------------------------------
            title=title.strip()



            #-------------------------------------
            # 3. Clean DOI
            #-------------------------------------
            if doi:
                doi= doi.strip().lower()



            #-------------------------------------
            # 4. Remove Duplicate DOI
            #-------------------------------------
            if doi:
                if doi in seen_dois:
                    continue
                seen_dois.add(doi)



            #-------------------------------------
            # 5. Normalize Year
            #-------------------------------------
            if year:
                try:
                    year=int(year)
                except (ValueError, TypeError):
                    year= None



            #-------------------------------------
            # 6. Create Cleaned Paper
            #-------------------------------------
            cleaned_paper = {
                "title": title,
                "year": year,
                "doi": doi,
                "cited_by_count": paper.get("cited_by_count", 0),
                "openalex_id": paper.get("openalex_id")


            }

        cleaned_papers.append(cleaned_paper)

        # save  cleaned data
        with open(output_file, "w", encoding='utf-8') as file:
            json.dump(
                cleaned_papers,
                file,
                indent= 4,
                ensure_ascii= False
            )
        return cleaned_papers



            






