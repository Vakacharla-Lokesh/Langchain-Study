import os
import dotenv

dotenv.load_dotenv()

# from langchain.agents import create_agent
# from langchain.tools import tool
from langchain_core.runnables import RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama as Ollama

MODEL_NAME = os.environ.get("MODEL_NAME", "qwen3.5:4b")
BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

model = Ollama(model=MODEL_NAME, base_url=BASE_URL, temperature=0, max_tokens=512)

# from langchain_openrouter import ChatOpenRouter

# model = ChatOpenRouter(
#     model="qwen/qwen3.8-27b:free",
#     temperature=0,
#     max_tokens=1024,
#     max_retries=2,
# )

# Prompts
tweet_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a twitter assistant.

            Rules:
            1. Generate a twitter post based on the user's topic.
            2. The post must be concise and engaging.
            3. No introduction.
            4. No conclusion.
            """
        ),
        ("human", "{topic}")
    ]
)

linkedin_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a LinkedIn assistant.

            Rules:
            1. Generate a LinkedIn post based on the user's topic.
            2. The post must be concise, professional, and engaging.
            3. No introduction.
            4. No conclusion.
            """
        ),
        ("human", "{topic}")
    ]
)

haiku_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a haiku assistant.

            Rules:
            1. Generate a haiku based on the user's topic.
            2. The haiku must be in the traditional 5-7-5 syllable pattern.
            3. No introduction.
            4. No conclusion.
            5. Output only the haiku.
            """
        ),
        ("human", "{topic}")
    ]
)

# LCEL Chain
parallel_chain = RunnableParallel(
    tweet = tweet_prompt | model | StrOutputParser(),
    linkedin = linkedin_prompt | model | StrOutputParser(),
    haiku = haiku_prompt | model | StrOutputParser(),
)

def main():
    print("Invoking parallel chain with topic: 'AI Engineer jobs in the Bay Area'")
    result = parallel_chain.invoke({"topic":"AI Engineer jobs in the Bay Area"})
    print("Result:")
    print(result)

if __name__ == "__main__":
    main()