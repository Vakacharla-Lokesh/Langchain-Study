import os
import dotenv

dotenv.load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM as Ollama

MODEL_NAME = os.environ.get("MODEL_NAME", "qwen3.5:4b")
BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

model = Ollama(model=MODEL_NAME, base_url=BASE_URL, temperature=0, max_tokens=512)

# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a concise summarization assistant.
             
            Rules:
            1. Summarize the user's text in EXACTLY 3 bullet points.
            2. Each bullet must be concise.
            3. No introduction.
            4. No conclusion.
            5. Output only the bullets.
            """
        ),
        ("human", "{text}")
    ]
)

# LCEL Chain
chain = prompt | model | StrOutputParser()

# Input text
# text = input("\nPaste text to summarize: ")

# Define the text to be summarized
text = """
Neon Genesis Evangelion (Japanese: 新世紀エヴァンゲリオン, Hepburn: Shin Seiki Evangerion; lit. 'New Century Evangelion' in Japanese and lit. 'New Beginning Gospel' in Greek), also known as simply Evangelion or Eva, is a Japanese anime television series produced by Gainax and Tatsunoko Production, and directed by Hideaki Anno. It was broadcast on TV Tokyo and its affiliates from October 1995 to March 1996. The story, set in 2015, fifteen years after a worldwide cataclysm in the futuristic fortified city of Tokyo-3, follows Shinji Ikari, a teenage boy who is recruited by his father Gendo Ikari to the mysterious organization Nerv. Shinji is tasked to pilot an Evangelion, a giant biomechanical mecha, to fight and destroy beings known as Angels.",
    "The series has been described as a deconstruction of the mecha genre; it delves into the experiences, emotions, and mental health of the Evangelion pilots and Nerv members as they are called upon to understand the ultimate cause of events and the motives behind human action. The series features archetypal imagery derived from Shinto cosmology and mystical Judeo-Christian religions and traditions, including Midrashic tales and Kabbalah.[4] The psychoanalytic accounts of human behavior put forward by Sigmund Freud and Carl Jung are also prominently featured.[5][6]",
    "Neon Genesis Evangelion received acclaim from critics and audiences and is regarded as one of the greatest animated series of all time; however, its final two episodes drew controversy, as many viewers found the ending confusing and abstract. Gainax attributed the episodes' abstract style both to the severe time constraints imposed by the production schedule and to Anno's deliberate artistic choice. In 1997, Gainax released a remake of the last two episodes in the feature film The End of Evangelion, written and co-directed by Anno. A series of four films, Rebuild of Evangelion, retelling the events of the series with different plot elements and a new ending, were released between 2007 and 2021. Evangelion has had a profound influence on the anime industry and influenced numerous future works. Films, manga, home video releases, and other products in the franchise have achieved record sales in Japanese markets and strong sales in overseas markets, with related goods earning over ¥150 billion by 2007 and Evangelion pachinko machines generating ¥700 billion by 2015.\n\n")
"""
# Invoke chain
result = chain.invoke(
{
"text": text
}
)

print("\nSummary:\n")
print(result)