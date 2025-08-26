import os
from dotenv import load_dotenv
from typing import Any, Dict

from langchain_community.chat_models import ChatLiteLLM
from langchain.chains import ConversationChain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

# --- 1. Load environment variables from a .env file ---
# This is a best practice for managing configuration and sensitive data.
# Create a file named `.env` in the same directory as this script and add:
# BASE_URL="http://localhost:11434"
# MODEL_PROVIDER="ollama"
# MODEL_NAME="qwen2.5:1.5b"
load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:11434")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:1.5b")

# Optional: Add a check to ensure the variables are loaded
if not BASE_URL:
    print("Error: BASE_URL is not set. Please check your .env file or environment.")
    exit()

# --- 2. Initialize the LiteLLM model for Ollama ---
# To use an Ollama model with LiteLLM, you must prefix the model name
# with "ollama/". This tells LiteLLM to route the request to your
# local Ollama server.
llm = ChatLiteLLM(
    model=f"{MODEL_PROVIDER}/{MODEL_NAME}",
    api_base=BASE_URL,
    temperature=0.6,
    max_tokens=256
)

# --- 3. Set up memory for the agent ---
# Memory is crucial for a chatbot to remember past turns in a conversation.
# ConversationBufferMemory stores the entire chat history.
memory = ConversationBufferMemory(
    memory_key="chat_history", 
    return_messages=True
)

# --- 4. Create the conversation prompt ---
# This is a much simpler prompt since we're no longer using tools.
# We explicitly tell the model that the history is present.
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "The following is a friendly conversation between a human and an AI. If you do not have the information to answer a question, please respond with 'I cannot answer that question.'"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ]
)


# --- 5. Create a simple conversational chain ---
# We use `ConversationChain` to handle the prompt, LLM, and memory.
# It's a much simpler way to create a conversational agent without tools.
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=True,
)

# --- 6. Start the conversational loop with error handling ---
print("Chatbot initialized. Type 'exit' to end the conversation.")
while True:
    try:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Ending conversation.")
            break
        
        # The `invoke` method runs the conversational chain with the user's input.
        response = conversation.invoke({"input": user_input})
        print(f"Agent: {response['response']}")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please try again or type 'exit' to quit.")
