from typing import Dict, List
from litellm import completion
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

MODEL_PROVIDER = "openai"
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
API_KEY = os.getenv("OPENAI_API_KEY")


def generate_response(messages: List[Dict]) -> Dict:
    """Call OpenAI via LiteLLM and return full response as a Python dict."""
    response = completion(
        model=f"{MODEL_PROVIDER}/{MODEL_NAME}",
        messages=messages,
        api_key=API_KEY,
    )
    return response  # type: ignore


def get_response_content(response: Dict) -> str:
    """Safely extract content from any LLM response."""
    try:
        return response.choices[0].message.content  # type: ignore
    except AttributeError:
        return response.choices[0].message.get("content", "")  # type: ignore


def main():
    context = """
        You are Hasan's Python coding assistant and expert software engineer.
        Your primary role is to help with Python tasks: writing code, debugging,
        and explaining Python concepts.

        You cannot answer questions unrelated to Python unless the question
        is explicitly about this chatbot, its behavior, or usage.

        - Python questions: answer clearly and concisely.
        - Chatbot questions: general explanation allowed.
        - Any other topic: respond strictly:
        "I am sorry! I am a Python coding assistant and cannot answer this question."
    """

    while True:
        user_input = input("\nAsk me something (type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": user_input},
        ]

        try:
            response = generate_response(messages)
            text = get_response_content(response)
            print("\nResponse:", text)
            print("Total tokens used:", getattr(response.usage, "total_tokens", "N/A"))  # type: ignore
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
