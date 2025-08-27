import pyttsx3
import speech_recognition as sr
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
import pyaudio # required for speech recognition

# Initialize the LLM model
llm = OllamaLLM(model="qwen2.5:1.5b")

# Initialize chat history (assuming you're using LangChain)
chat_history = ChatMessageHistory()

# Initialize PyAudio module for speech recognition
recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.0
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True

def speak(text):
    """
    Speaks the given text using the pyttsx3 library.

    Args:
        text (str): Text to be spoken
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    """
    Listens to the microphone and returns a string of what the user said.

    Recognizes speech using Google Speech Recognition. If the speech is not recognized,
    it will print an error message and return None.

    Returns:
        str: Recognized speech
    """
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
            
        try:
            query = recognizer.recognize_google(audio)  # type: ignore
            print("You said:", query.lower())
            return query.lower()
        except sr.UnknownValueError:
            print("I Could not understand the voice. Please try again!")
            return None  # Changed from "" to None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"Error during listening: {e}")
        return None

# AI Chat prompt (fixed spelling)
prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="Previous Conversation: {chat_history}\nUser: {question}\nAI:",  # Fixed template
)

# Function to run the LLM chain and generate response
def run_chain(question):
    """
    Runs the LLM chain to generate a response to the user's question.

    Args:
        question (str): User's question

    Returns:
        str: AI's response
    """
    chat_history_text = "\n".join(
        [f"{msg.type.capitalize()}: {msg.content}" for msg in chat_history.messages]
    )
    
    response = llm.invoke(prompt.format(chat_history=chat_history_text, question=question))
    chat_history.add_user_message(question)
    chat_history.add_ai_message(response)
    return response

# Initialize the speech recognition loop
while True:
    query = listen()
    if query is None:
        continue
    
    # Check for exit commands
    if any(word in query for word in ['exit', 'quit', 'goodbye', 'bye', 'stop']):
        speak("Goodbye! Have a Great Day!")
        break

    # Process the user input through the LLM chain and generate response
    print(f"User: {query}")
    response = run_chain(query)
    print(f"Personal Assistant: {response}")
    
    # Speak back to the user using pyttsx3
    speak(response)

print("Goodbye!")
