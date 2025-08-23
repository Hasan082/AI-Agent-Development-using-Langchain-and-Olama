from litellm import completion
from typing import List, Dict
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:11434")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:1.5b")


def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response"""
    response = completion(
        model=f"{MODEL_PROVIDER}/{MODEL_NAME}",
        messages=messages,
        api_base=BASE_URL,
        max_tokens=600,
    )
    return response  # type: ignore


messages = [
    {
        "role": "system",
        "content": "You are an expert software engineer that prefers functional programming.",
    },
    {
        "role": "user",
        "content": "Write a function to swap the keys and values in a dictionary.",
    },
]

# First Answer
response = generate_response(messages)
print(response.choices[0].message.content)  # type: ignore
print(f"First answer end here")  # type: ignore
print("--" * 20)
time.sleep(20)
# PROMPT 1
messages = [
    # Here is the assistant's response from the previous step
    # with the code. This gives it "memory" of the previous
    # interaction.
    {
        "role": "assistant",
        "content": response.choices[0].message.content,  # type: ignore
    },  #     type: ignore
    # Now, we can ask the assistant to update the function
    {"role": "user", "content": "Update the function to include documentation."},
]

# Second Answer with memory
print(response.choices[0].message.content)  # type: ignore
print(f"Output tokens: {response.usage.completion_tokens}")  # type: ignore
