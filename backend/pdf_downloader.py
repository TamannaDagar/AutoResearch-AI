import requests
from pathlib import Path


def download_pdf(pdf_url, output_path):
    """
    Download a PDF from an accessible URL.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(
        pdf_url,
        timeout=30
    )

    response.raise_for_status()

    content_type = response.headers.get(
        "Content-Type",
        ""
    ).lower()

    if (
        "pdf" not in content_type
        and not response.content.startswith(b"%PDF")
    ):
        raise ValueError(
            "The URL did not return a PDF."
        )

    with open(output_path, "wb") as file:
        file.write(response.content)

    return output_path