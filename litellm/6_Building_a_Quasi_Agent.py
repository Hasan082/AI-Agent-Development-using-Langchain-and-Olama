# Building a Mini-Code-Agent

# For practice, we are going to write a quasi-agent that can write Python functions based on user requirements. It isn’t quite a real agent, it can’t react and adapt, but it can do something useful for us.

# The quasi-agent will ask the user what they want code for, write the code for the function, add documentation, and finally include test cases using the unittest framework. This exercise will help you understand how to maintain context across multiple prompts and manage the information flow between the user and the LLM. It will also help you understand the pain of trying to parse and handle the output of an LLM that is not always consistent.

# ==============================================================================================================

# Practice Exercise

# ==============================================================================================================

# This exercise will allow you to practice programmatically sending prompts to an LLM and managing memory.

# For this exercise, you should write a program that uses sequential prompts to generate any Python function based on user input. The program should:

# ==============================================================================================================

# First Prompt:


# Ask the user what function they want to create
# Ask the LLM to write a basic Python function based on the user’s description
# Store the response for use in subsequent prompts
# Parse the response to separate the code from the commentary by the LLM
# Second Prompt:

# ==============================================================================================================

# Pass the code generated from the first prompt
# Ask the LLM to add comprehensive documentation including:
# Function description
# Parameter descriptions
# Return value description
# Example usage
# Edge cases
# Third Prompt:

# ==============================================================================================================

# Pass the documented code generated from the second prompt
# Ask the LLM to add test cases using Python’s unittest framework
# Tests should cover:
# Basic functionality
# Edge cases
# Error cases
# Various input scenarios
# Requirements:

# ==============================================================================================================

# Use the LiteLLM library
# Maintain conversation context between prompts
# Print each step of the development process
# Save the final version to a Python file
# If you want to practice further, try using the system message to force the LLM to always output code that has a specific style or uses particular libraries.

# ==============================================================================================================
# SOLUTION
# ==============================================================================================================
from litellm import completion
from typing import List, Dict
import os
from dotenv import load_dotenv
import time

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:11434")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:1.5b")


def generate_response(messages: List[Dict[str, str]]) -> str:
    """Call LLM to get assistant's text content"""
    response = completion(
        model=f"{MODEL_PROVIDER}/{MODEL_NAME}",
        messages=messages,
        api_base=BASE_URL,
        max_tokens=1000,
    )
    return response.choices[0].message.content  # type: ignore


def extract_code_block(response_text: str) -> str:
    """Extract code block from LLM response"""
    if "```" not in response_text:
        return response_text.strip()
    code_block = response_text.split("```")[1].strip()
    if code_block.startswith("python"):
        code_block = code_block[6:].lstrip("\n")
    return code_block


def develop_custom_function():
    # Get user input
    print("\nWhat kind of function would you like to create?")
    print("Example: 'A function that calculates the factorial of a number'")
    function_description = input("Your description: ").strip()

    # Initialize conversation
    messages = [
        {
            "role": "system",
            "content": "You are a Python expert helping to develop a function.",
        }
    ]

    # --- Step 1: Generate initial function ---
    messages.append(
        {
            "role": "user",
            "content": f"Write a Python function that {function_description}. "
            f"Output the function in a ```python code block```.",
        }
    )
    initial_response = generate_response(messages)
    initial_function = extract_code_block(initial_response)
    print("\n=== Initial Function ===")
    print(initial_function)

    messages.append(
        {"role": "assistant", "content": f"```python\n{initial_function}\n```"}
    )

    # --- Step 2: Add documentation ---
    messages.append(
        {
            "role": "user",
            "content": "Add comprehensive documentation to this function, including description, "
            "parameters, return value, examples, and edge cases. "
            "Output the function in a ```python code block```.",
        }
    )
    documented_response = generate_response(messages)
    documented_function = extract_code_block(documented_response)
    print("\n=== Documented Function ===")
    print(documented_function)

    messages.append(
        {"role": "assistant", "content": f"```python\n{documented_function}\n```"}
    )

    # --- Step 3: Add unittest test cases ---
    messages.append(
        {
            "role": "user",
            "content": "Add unittest test cases for this function, including tests for basic functionality, "
            "edge cases, error cases, and various input scenarios. "
            "Output the code in a ```python code block```.",
        }
    )
    test_cases_response = generate_response(messages)
    test_cases = extract_code_block(test_cases_response)
    print("\n=== Test Cases ===")
    print(test_cases)

    # --- Step 4: Save to file ---
    filename = function_description.lower()
    filename = "".join(c for c in filename if c.isalnum() or c.isspace())
    filename = filename.replace(" ", "_")[:30] + ".py"

    with open(filename, "w") as f:
        f.write(f"{documented_function}\n\n{test_cases}")

    print(f"\nFinal code has been saved to {filename}")
    return documented_function, test_cases, filename


if __name__ == "__main__":
    develop_custom_function()
