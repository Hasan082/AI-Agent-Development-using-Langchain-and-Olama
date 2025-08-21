from typing import Dict, List
from litellm import completion
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:11434")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:1.5b")


def generate_response(messages: List[Dict]) -> Dict:
    """Call LLM via LiteLLM and return full response as a Python dict."""
    response = completion(
        model=f"{MODEL_PROVIDER}/{MODEL_NAME}",
        messages=messages,
        api_base=BASE_URL,
    )
    return response  # type: ignore


def get_response_content(response: Dict) -> str:
    """Safely extract content from any LLM response."""
    try:
        return response.choices[0].message.content # type: ignore
    except AttributeError:
        # fallback for Ollama/OpenAI
        return response.choices[0].message.get("content", "") # type: ignore


while True:
    user_input = input("What do you want to ask me? For Stop type 'exit': ")
    if user_input.lower() == "exit":
        break

    context = """
        You are Hasan's coding assistant and expert software engineer. 
        Your primary role is to help with **Python programming tasks**: writing code, debugging, 
        and explaining Python concepts.

        You **cannot answer questions unrelated to Python** unless the question is explicitly about this chatbot, 
        its behavior, or how it works.

        - If a user asks a Python question, provide a clear, correct, and concise answer.
        - If a user asks about the chatbot itself, you may give a general explanation.
        - For any other topic, respond strictly:
        "I am sorry! I am a Python coding assistant and cannot answer this question."
    """


    messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": user_input},
    ]

    try:
        response = generate_response(messages)
        text = get_response_content(response)
        print(text)
        print("Total tokens used:", getattr(response.usage, "total_tokens", "N/A")) # type: ignore
    except Exception as e:
        print("Error:", e)
