import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from models.product_schema import Product

from google import genai
from google.genai import types
from dotenv import load_dotenv




load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Please add it to your .env file."
    )


client = genai.Client(api_key=API_KEY)


def extract_product_information(pages):

    document_text = ""

    for page in pages:
        document_text += (
            f"\n\n--- PAGE {page['page']} ---\n"
            f"{page['text']}"
        )

    prompt = f"""
You are an industrial product data extraction system.

Analyze the following product document.

Your job is to extract ONLY information that is supported
by the document.

IMPORTANT RULES:

1. Do not invent specifications.
2. Do not guess missing values.
3. Preserve the original value and unit.
4. For every specification, provide the exact source text
   supporting the value when possible.
5. Provide the page number where the specification appears.
6. Applications and industries must only be included when
   supported by the document.
7. If information is missing, leave it empty.
8. Distinguish facts from assumptions.

DOCUMENT:

{document_text}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Product,
        ),
    )

    if response.parsed:
        return response.parsed

    raise ValueError("Gemini did not return structured product data.")