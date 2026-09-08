import json
from sentence_transformers import SentenceTransformer

MODEL_NAME= 'all-miniLM-L6-v2'

def load_chunks(input_file):
    with open(input_file, "r", encoding='utf-8') as file:
        return json.load(file)


def create_embeddings(chunks):
    model= SentenceTransformer(MODEL_NAME)


    texts= [chunk['text'] for chunk in chunks]

    embeddings= model.encode(
        texts,
        show_progress_bar= True
    )
    return embeddings

if __name__== "__main__":
    input_file= "data/papers/chunks/test_paper_chunks.json"

    chunks= load_chunks(input_file)

    print("Total Chunks:", len(chunks))

    embeddings= create_embeddings(chunks)

    print("Embedding creation successful!")
    print("Number of embeddings:", len(embeddings))
    print("Embedding dimension:", len(embeddings[0]))
