from langchain_ollama import OllamaLLM

llm = OllamaLLM(model='mistral')


print("Welcome to Our AI Agent! Ask me anything about our services!")

while True:
    question = input("Your question or type \'exit\' to stop chating: ")
    
    if question.lower().strip() == 'exit':
        print("GoodBye")
        break
    
    answer = llm.invoke(question)
    
    print(f"AI Agent: {answer}")
    print()
    