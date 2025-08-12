from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

# Load AI
llm = OllamaLLM(model="mistral")

# Initialize Memory
chat_history = ChatMessageHistory()

# AI Chat Pronpt
prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="Prevous Conversion: {chat_history}\n User: {question} AI",
)


def run_chain(question):
    # Load chat history text
    chat_history_text = "\n".join(
        [f"{msg.type.capitalize()}: {msg.content}" for msg in chat_history.messages]
    )
    response = llm.invoke(
        prompt.format(chat_history=chat_history_text, question=question)
    )

    chat_history.add_user_message(question)
    chat_history.add_ai_message(response)

    return response


print("Your AI Assistant with Memory")
print("Chatboot with memory! Ask me anything about our services!")
print("Type 'exit' for stop chat")


while True:
    user_input = input("You: ")

    if user_input.lower().strip() == "exit":
        print("Goodbye Today")
        break

    ai_response = run_chain(user_input)

    print(f"AI Bot: {ai_response}")
    print()


# ToDo: https://gale.udemy.com/course/mastering-ai-agents-bootcamp-build-smart-chatbots-tools/learn/lecture/48844581#overview
