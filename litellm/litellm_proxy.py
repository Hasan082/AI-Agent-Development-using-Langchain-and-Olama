from typing import Dict, List
from litellm import completion
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:11434")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

python_context = """
You are Hasan's Python coding assistant.
Answer only Python-related questions: coding, debugging, or explaining concepts.
If a question is unrelated, reply:
"I am sorry! I am a Python coding assistant and cannot answer this."
"""

general_context = """
You are Hasan's general knowledge assistant.
You can answer any general questions.
If a question is about coding, give concise Python guidance.
"""

def generate_response(messages: List[Dict]) -> Dict:
    response = completion(
        model=f"{MODEL_PROVIDER}/{MODEL_NAME}",
        messages=messages,
        api_base=BASE_URL,
    )
    return response  # type: ignore

def get_response_content(response: Dict) -> str:
    try:
        return response.choices[0].message.content  # type: ignore
    except AttributeError:
        return response.choices[0].message.get("content", "")  # type: ignore

def run_chat():
    while True:
        # Let the user pick the context
        mode = input("Choose mode: (1) Python assistant, (2) General assistant, or 'exit': ")
        if mode.lower() == "exit":
            break

        selected_context = python_context if mode == "1" else general_context

        user_input = input("Your question: ")
        if user_input.lower() == "exit":
            break

        messages = [
            {"role": "system", "content": selected_context},
            {"role": "user", "content": user_input},
        ]

        try:
            response = generate_response(messages)
            text = get_response_content(response)
            print(text)
            print("Total tokens used:", getattr(response.usage, "total_tokens", "N/A"))  # type: ignore
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    run_chat()
