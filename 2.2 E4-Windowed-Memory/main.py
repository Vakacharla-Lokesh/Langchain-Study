import os
from dotenv import load_dotenv

load_dotenv()

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser

MODEL_NAME = os.environ.get("MODEL_NAME", "deepseek-r1:1.5b")
BASE_URL = os.environ.get("BASE_URL", "http://localhost:11434")

WINDOW = 2
history = []

SYSTEM_PROMPT = """You are a helpful assistant that answers questions."""

# Initialize the ChatOllama model
chat_model = ChatOllama(model=MODEL_NAME, base_url=BASE_URL, temperature=0, max_tokens=512)

def main():
    print("Hello from 2-2-e4-windowed-memory!")

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Add the user's message to the history
        history.append(HumanMessage(content=user_input))

        # Keep only the last WINDOW messages in history
        windowed_history = history[-WINDOW:]

        # Create a list of messages to send to the model
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + windowed_history

        # Get the model's response
        response = (chat_model | StrOutputParser()).invoke(messages)

        # Print the model's response
        print(f"Model: {response}")


if __name__ == "__main__":
    main()
