from litellm import completion
from typing import List, Dict
import os
from dotenv import load_dotenv
import time

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:11434")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:1.5b")


def generate_response(messages: List[Dict]) -> Dict:
    """Call LLM to get response"""
    response = completion(
        model=f"{MODEL_PROVIDER}/{MODEL_NAME}",
        messages=messages,
        api_base=BASE_URL,
        max_tokens=600,
    )
    return response # type: ignore


# Start conversation history
messages: List[Dict] = [
    {
        "role": "system",
        "content": "You are an expert software engineer that prefers functional programming.",
    },
    {
        "role": "user",
        "content": "Write a function to swap the keys and values in a dictionary.",
    },
]

# First answer
response = generate_response(messages)
answer = response.choices[0].message.content  # type: ignore
print(answer)
print("First answer end here")
print("--" * 20)

# Add assistant reply to history
messages.append({"role": "assistant", "content": answer})

time.sleep(5)

# Second user question (with memory intact)
messages.append({"role": "user", "content": "What was my question?"})
response = generate_response(messages)
answer = response.choices[0].message.content  # type: ignore

print(answer)
print(f"Completion tokens used: {response.usage.completion_tokens}")  # type: ignore
