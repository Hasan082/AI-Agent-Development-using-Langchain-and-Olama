from litellm import completion
import pyttsx3
import speech_recognition as sr
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
import pyaudio # required for speech recognition
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import pyttsx3
import os
import pygame
import time

MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:1.5b")
BASE_URL = os.getenv("BASE_URL", "http://localhost:11434")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")


# Create a wrapper for LiteLLM
def query_llm(prompt: str) -> str:
    response = completion(
        model=f"{MODEL_PROVIDER}/{MODEL_NAME}",
        messages=[{"role": "user", "content": prompt}],
        api_base=BASE_URL  # for Ollama
    )
    return response["choices"][0]["message"]["content"] # type: ignore



# Initialize chat history (assuming you're using LangChain)
chat_history = ChatMessageHistory()

# Initialize PyAudio module for speech recognition
recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.0
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True


# PC local voice
# def speak(text):
#     """
#     Speaks the given text using the pyttsx3 library.

#     Args:
#         text (str): Text to be spoken
#     """
#     engine = pyttsx3.init()
#     mp3_fp = BytesIO()
#     tts_en = gTTS(text, lang='en')
#     tts_en.write_to_fp(mp3_fp)
#     engine.say(text)
#     engine.runAndWait()


# google voice
# def speak(text: str):
#     """
#     Speaks the given text using gTTS and plays from memory (no temp file).
#     """
#     mp3_fp = BytesIO()
#     tts = gTTS(text, lang='en')
#     tts.write_to_fp(mp3_fp)
#     mp3_fp.seek(0)

#     audio = AudioSegment.from_file(mp3_fp, format="mp3")
#     play(audio)
pygame.init()

def speak(text: str):
    tts = gTTS(text=text, lang='en')
    speech_file = "output.mp3"
    tts.save(speech_file)

    # Play the output audio using pygame
    pygame.mixer.music.load(speech_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(1)
    
    
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
            audio = recognizer.listen(source, timeout=4, phrase_time_limit=5)
            
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
    
    response = query_llm(prompt.format(chat_history=chat_history_text, question=question))
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
    response = run_chain(query)
    print(f"Personal Assistant: {response}")
    speak(response)
    

print("Goodbye!")
