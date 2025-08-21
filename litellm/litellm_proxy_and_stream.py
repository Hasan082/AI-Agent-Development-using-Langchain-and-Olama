from typing import Dict, List
from litellm import completion
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:11434")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:1.5b")

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

def generate_response_stream(messages: List[Dict]):
    """Call LiteLLM with streaming and yield tokens as they arrive."""
    stream = completion(
        model=f"{MODEL_PROVIDER}/{MODEL_NAME}",
        messages=messages,
        api_base=BASE_URL,
        stream=True,
    )

    for event in stream:
        event_type = getattr(event, "type", None)
        if event_type == "delta":
            yield getattr(event, "delta", "")
        elif event_type == "done":
            break

def run_chat():
    selected_context = python_context
    print("Chat started. Type 'change' to switch context (Python <-> General), 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "change":
            # Switch context
            if selected_context == python_context:
                selected_context = general_context
                print("Context switched to General assistant.\n")
            else:
                selected_context = python_context
                print("Context switched to Python assistant.\n")
            continue

        messages = [
            {"role": "system", "content": selected_context},
            {"role": "user", "content": user_input},
        ]

        try:
            print("Assistant:", end=" ", flush=True)
            for token in generate_response_stream(messages):
                print(token, end="", flush=True)
            print("\n")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run_chat()
