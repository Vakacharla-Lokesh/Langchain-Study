import os
from dotenv import load_dotenv

load_dotenv()

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool


MODEL_NAME = os.environ.get("MODEL_NAME", "qwen3.5:4b")
BASE_URL = os.environ.get("BASE_URL", "http://localhost:11434")

SYSTEM_PROMPT = """You are a helpful assistant with access to various tools to help answer the user's questions."""

chat_model = ChatOllama(model=MODEL_NAME, base_url=BASE_URL, temperature=0, max_tokens=512)

@tool
def add(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers together."""
    return a * b


def main():
    print("Hello from 3-1-e5-first-tool-call!")

    tools = [add, multiply]
    chat_model_with_tools = chat_model.bind_tools(tools, tool_choice="required")
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content="What is 5 * 3? Use an available tool to answer the question."),
    ]

    response = chat_model_with_tools.invoke(messages)
    if not response.tool_calls:
        raise RuntimeError(
            f"{MODEL_NAME} returned no tool call. Try a model with reliable tool-calling support."
        )

    messages.append(response)
    tools_by_name = {tool.name: tool for tool in tools}
    for tool_call in response.tool_calls:
        result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
        messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))

    response = chat_model.invoke(messages)

    print(f"Response: {response.content}")


if __name__ == "__main__":
    main()
