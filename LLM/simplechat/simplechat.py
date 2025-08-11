from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

# Load AI 
llm = OllamaLLM(model="mistral")

# Initialize Memory
chat_history = ChatMessageHistory()

# AI Chat Pronpt
promots = PromptTemplate(
    input_variables=['chat_history', 'question'],
    template="Prevous Conversion: {chat_history}\n User: {question} AI"    
)

def run_chain(question):
    # Load chat history text
    chat_history_text = "/n".join([f"{msg.type.capitalize()}" for msg in chat_history.messages])






# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_core.prompts import PromptTemplate
# from langchain_ollama import OllamaLLM

# # Load the AI Model
# llm = OllamaLLM(model="mistral")

# # Initiate Hiostory
# chat_history = ChatMessageHistory()

# prompt = PromptTemplate(
#     input_variables=["chat_history", "question"],
#     template="Prevoius Conversion: {chat_history}\nUser:m {question}\n AI",
# )


# def run_chain(question):
#     chat_history_text = "\n".join(
#         f"{msg.type.capitalize()}: {msg.content}" for msg in chat_history.messages
#     )
#     response = llm.invoke(
#         prompt.format(chat_history=chat_history_text, question=question)
#     )

#     chat_history.add_user_message(question)
#     chat_history.add_ai_message(response)

#     return response


# print("Chatboot with memory! Ask me anything about our services!")

# while True:
#     question = input("Your question or type 'exit' to stop chating: ")

#     if question.lower().strip() == "exit":
#         print("GoodBye")
#         break

#     answer = llm.invoke(question)

#     print(f"AI Agent: {answer}")
#     print()
