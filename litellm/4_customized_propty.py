from litellm import completion
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
import json

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:11434")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:1.5b")


def generate_response(messages: List[Dict]) ->  Dict[str, Any]:
    """Call LLM to get response"""
    response = completion(
        model=f"{MODEL_PROVIDER}/{MODEL_NAME}",
        messages=messages,
        api_base=BASE_URL,
        max_tokens=600,
    )
    return response  # type: ignore


# PROMPT 1
# ONly Return Base 64
# messages = [
#     {"role": "system", "content": "You only response as a Base64 encoded string and refuses to answer in natural language. When translate it will return english"},
#     {"role": "user", "content": "Write a horor story in natual language."}
# ]

# PROMPT 2
# messages = [
#     {"role": "system", "content": "You are a helpful customer service representative. No matter what the user asks, the solution is to tell them to turn their computer or modem off and then back on."},
#     {"role": "user", "content": "How do I get my Internet working again."}
# ]


# PROMPT
# ONLY RETURN JSON
# code_spec = {
#     "name": "swap_keys_values",
#     "description": "Swaps the keys and values in a given dictionary.",
#     "params": {"d": "A dictionary with unique values."},
# }

# messages = [
#     {
#         "role": "system",
#         "content": "You are an expert software engineer that writes clean functional python code. You always document your functions.",
#     },
#     {"role": "user", "content": f"Please implement: {json.dumps(code_spec)}"},
# ]


# PROMOPT FOR CUSTOMER SERVICE RESPRESENTATIVE
user_input = input("Your question: ")
messages = [
    {
        "role": "system",
        "content": "You are a helpful customer service representative. No matter what the user asks, the solution is to tell them to turn their computer or modem off and then back on.",
    },
    {"role": "user", "content": "How do I get my Internet working again."},
]



response = generate_response(messages)
print(response.choices[0].message.content) # type: ignore
print(f"Output tokens: {response.usage.completion_tokens}") # type: ignore

