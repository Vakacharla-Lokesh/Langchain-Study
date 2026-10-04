import os
import dotenv

dotenv.load_dotenv()

from langchain.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama as Ollama
from pydantic import ValidationError
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json


PRIMARY_MODEL_NAME = os.environ.get("MODEL_NAME", "deepseek-r1:latest")
BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

primary_model = Ollama(model=PRIMARY_MODEL_NAME, base_url=BASE_URL, temperature=0, max_tokens=512)

examples = [
    {"input": "I love this laptop, fast and light",
     "output": '{"sentiment": "positive", "keywords": ["fast", "light"]}'},
    {"input": "Terrible battery life, disappointed",
     "output": '{"sentiment": "negative", "keywords": ["battery life"]}'},
]

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=PromptTemplate.from_template("Input: {input}\nOutput: {output}"),
    prefix="Classify sentiment and extract keywords as JSON, matching the exact format below.",
    suffix="Input: {input}\nOutput:",
    input_variables=["input"],
)

SYSTEM_PROMPT = """
You extract structured information from customer reviews.

Determine:
- sentiment: positive, negative, or mixed
- keywords: every specific keyword mentioned in the review

Structure your output as a JSON object with the following format:
{
  "sentiment": "<sentiment>",
  "keywords": ["<keyword1>", "<keyword2>", ...]
}
"""

def main():

    review = "The camera quality is amazing, but the battery drains quickly."

    chain = few_shot_prompt | primary_model | StrOutputParser()
    
    raw = chain.invoke({"input": review})
    parsed = json.loads(raw)

    print(f"Review: {review}")
    print(f"Raw output: {raw}")
    print(f"Parsed output: {parsed}")
    # messages = [
    #     SystemMessage(content=SYSTEM_PROMPT),
    #     HumanMessage(content=review)
    # ]

    # print(f"Review: {review}")

    # print(f"Messages: {messages}")

    # primary_output = primary_model.invoke(messages)

    # print(f"Primary output: {primary_output}")
        # try:
        #     data = ReviewExtract.model_validate_json(primary_output)

        #     print(data)
        # except ValidationError as e:
        #     print(f"Primary model failed: {e}")
        #     print("-" * 50)
    print("-" * 50)


if __name__ == "__main__":
    print(f"Using primary model: {PRIMARY_MODEL_NAME}")
    main()