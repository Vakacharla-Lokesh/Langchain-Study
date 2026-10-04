import os
import dotenv

dotenv.load_dotenv()

from langchain.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama as Ollama
from pydantic import ValidationError

from schemas import ReviewExtract

PRIMARY_MODEL_NAME = os.environ.get("MODEL_NAME", "qwen3.5:4b")
SECONDARY_MODEL_NAME = os.environ.get("SECONDARY_MODEL_NAME", "qwen3.5:4b")
BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

primary_model = Ollama(model=PRIMARY_MODEL_NAME, base_url=BASE_URL, temperature=0, max_tokens=512)
secondary_model = Ollama(model=SECONDARY_MODEL_NAME, base_url=BASE_URL, temperature=0, max_tokens=512)

SYSTEM_PROMPT = """
You extract structured information from restaurant reviews.

Determine:
- sentiment: positive, negative, or mixed
- dishes_mentioned: every specific dish mentioned in the review
- rating_out_of_5: the rating explicitly stated in the review

Do not invent a rating when the review does not provide one.
"""

#MODELS WITH STRUCTURED OUTPUT
primary_model_structured = primary_model.with_structured_output(ReviewExtract)
secondary_model_structured = secondary_model.with_structured_output(ReviewExtract)

with open("reviews.txt", "r") as f:
    reviews = [line.strip() for line in f if line.strip()]   

def main():
    for review in reviews:

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=review)
        ]

        print(f"Review: {review}")

        print("Primary Model Output:")

        primary_output = primary_model_structured.invoke(messages)

        try:
            data = ReviewExtract.model_validate_json(primary_output)

            print(data)
        except ValidationError as e:
            print(f"Primary model failed: {e}")
            print("-" * 50)
            secondary_output = secondary_model_structured.invoke(messages)
            try:
                data = ReviewExtract.model_validate_json(secondary_output)
                print("Secondary Model Output:")
                print(data)
            except ValidationError as e:
                print(f"Secondary model failed: {e}")

        print("-" * 50)


if __name__ == "__main__":
    print(f"Using primary model: {PRIMARY_MODEL_NAME}")
    print(f"Using secondary model: {SECONDARY_MODEL_NAME}")
    main()