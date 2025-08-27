import pyttsx3
import speech_recognition as sr
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
import streamlit as st
import threading

# ---------------- Models & Memory ----------------
llm = OllamaLLM(model="qwen2.5:1.5b")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()
if 'ai_speaking' not in st.session_state:
    st.session_state.ai_speaking = False

prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="Previous Conversation: {chat_history}\nUser: {question}\nAI:",
)

# ---------------- Speech Setup ----------------
recognizer = sr.Recognizer()
recognizer.energy_threshold = 200
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8

engine = pyttsx3.init()
engine.setProperty('rate', 175)

# ---------------- Functions ----------------
def speak(text):
    """Speak text in a separate thread to avoid blocking Streamlit."""
    def _speak():
        st.session_state.ai_speaking = True
        engine.say(text)
        engine.runAndWait()
        st.session_state.ai_speaking = False
    threading.Thread(target=_speak, daemon=True).start()

def listen():
    """Listen to the user's voice and return recognized text."""
    with sr.Microphone() as source:
        st.write("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)
    try:
        query = recognizer.recognize_google(audio)
        st.write(f"🧑 You said: {query}")
        return query
    except sr.UnknownValueError:
        st.write("❌ Could not understand your voice. Try again!")
        return ""
    except sr.RequestError as e:
        st.write(f"❌ Speech recognition service error: {e}")
        return ""

def run_chain(question):
    """Generate AI response and update chat history."""
    chat_history_text = "\n".join(
        [f"{msg.type.capitalize()}: {msg.content}" for msg in st.session_state.chat_history.messages]
    )
    response = llm.invoke(
        prompt.format(chat_history=chat_history_text, question=question)
    )
    st.session_state.chat_history.add_user_message(question)
    st.session_state.chat_history.add_ai_message(response)
    return response

def handle_voice_button():
    """Handle the press-to-talk button."""
    if st.session_state.ai_speaking:
        st.warning("🤖 AI is speaking, please wait...")
        return
    user_query = listen()
    if not user_query:
        return
    ai_response = run_chain(user_query)
    st.write(f"🧑 You: {user_query}")
    st.write(f"🤖 Assistant: {ai_response}")
    speak(ai_response)

# ---------------- Streamlit UI ----------------
st.title("🎙️ Voice Personal Assistant")
st.write("Powered by LangChain + Ollama")

st.button("🎤 Press to Talk", on_click=handle_voice_button, disabled=st.session_state.ai_speaking)

# Show chat history
st.subheader("Chat History")
for msg in st.session_state.chat_history.messages:
    if msg.type == "human":
        st.write(f"🧑 **You:** {msg.content}")
    else:
        st.write(f"🤖 **Assistant:** {msg.content}")

# Clear chat history
if st.button("🗑️ Clear Chat History"):
    st.session_state.chat_history.messages = []
