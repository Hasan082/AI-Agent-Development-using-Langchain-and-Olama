from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from litellm import completion
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
import os

# LiteLLM config
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:1.5b")
BASE_URL = os.getenv("BASE_URL", "http://localhost:11434")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")  # or "openai"

# FastAPI app
app = FastAPI()

# Chat history
chat_history = ChatMessageHistory()

# Prompt template
prompt_template = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="Previous Conversation: {chat_history}\nUser: {question}\nAI:"
)


# Add CORS middleware
origins = [
    "http://localhost:5500",  # your frontend URL
    "http://127.0.0.1:5500",  # sometimes necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # allow these origins
    allow_credentials=True,
    allow_methods=["*"],        # allow GET, POST, etc.
    allow_headers=["*"],        # allow all headers
)

# Pydantic model for request
class Query(BaseModel):
    query: str

# Endpoint to ask AI
@app.post("/ask")
def ask_ai(query: Query):
    # Prepare chat history
    chat_history_text = "\n".join(
        [f"{msg.type.capitalize()}: {msg.content}" for msg in chat_history.messages]
    )

    # Query LiteLLM
    response = completion(
        model=f"{MODEL_PROVIDER}/{MODEL_NAME}",
        messages=[{"role": "user", "content": prompt_template.format(chat_history=chat_history_text, question=query.query)}],
        api_base=BASE_URL
    )

    # Extract response text
    response_text = response["choices"][0]["message"]["content"]  # type: ignore

    # Update chat history
    chat_history.add_user_message(query.query)
    chat_history.add_ai_message(response_text)

    return {"response": response_text}
