import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = "gemini-3.8-flash"


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not set. "
            "Please check your .env file."
        )

    return genai.Client(api_key=api_key)


def generate_answer(prompt):
    client = get_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    test_prompt = """
    Answer the following question briefly:

    What is generative AI?
    """

    answer = generate_answer(test_prompt)

    print("\n===== GEMINI RESPONSE =====")
    print(answer)
    print("\n===== END RESPONSE =====")