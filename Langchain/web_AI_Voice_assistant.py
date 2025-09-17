import pyttsx3
import speech_recognition as sr
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
import streamlit as st
import threading
import queue

# ---------------- Models & Memory ----------------
llm = OllamaLLM(model="qwen2.5:1.5b")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()
if 'ai_speaking' not in st.session_state:
    st.session_state.ai_speaking = False

# Initialize thread-safe objects outside the main run loop
if 'stop_event' not in st.session_state:
    st.session_state.stop_event = threading.Event()
if 'speech_queue' not in st.session_state:
    st.session_state.speech_queue = queue.Queue()
if 'speak_thread' not in st.session_state:
    st.session_state.speak_thread = None

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
def speak_worker(stop_event, speech_queue):
    """Thread worker to speak text from a queue and handle interruptions."""
    while not stop_event.is_set():
        try:
            text = speech_queue.get(block=True, timeout=1)
            engine.say(text)
            engine.runAndWait()
            speech_queue.task_done()
        except queue.Empty:
            continue
        except RuntimeError:
            break

def start_speaker_thread():
    """Start the speaker thread once."""
    if st.session_state.speak_thread is None or not st.session_state.speak_thread.is_alive():
        st.session_state.speak_thread = threading.Thread(
            target=speak_worker,
            args=(st.session_state.stop_event, st.session_state.speech_queue),
            daemon=True
        )
        st.session_state.speak_thread.start()

def speak(text):
    """Add text to the speech queue."""
    st.session_state.speech_queue.put(text)
    st.session_state.ai_speaking = True

def listen():
    """Listen to the user's voice and return recognized text."""
    st.write("🎤 Listening...")
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
        query = recognizer.recognize_google(audio)
        st.write(f"🧑 You said: {query}")
        return query
    except sr.WaitTimeoutError:
        st.write("❌ No speech detected. Try again!")
        return ""
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
        st.warning("🤖 AI is speaking, please wait or press 'Stop AI'.")
        return
    user_query = listen()
    if not user_query:
        return
    ai_response = run_chain(user_query)
    st.write(f"🧑 You: {user_query}")
    st.write(f"🤖 Assistant: {ai_response}")
    speak(ai_response)
    st.rerun()

def handle_stop_button():
    """Interrupt ongoing AI speech."""
    if st.session_state.ai_speaking:
        engine.stop()
        with st.spinner("Stopping..."):
            while not st.session_state.speech_queue.empty():
                try:
                    st.session_state.speech_queue.get_nowait()
                except queue.Empty:
                    continue
                st.session_state.speech_queue.task_done()
        st.session_state.ai_speaking = False
        st.info("AI speech stopped.")
        st.rerun()
    else:
        st.info("No AI speech to stop.")

# ---------------- Streamlit UI ----------------
st.title("🎙️ Voice Personal Assistant")
st.write("Powered by LangChain + Ollama")

# Start the worker thread
start_speaker_thread()

col1, col2 = st.columns(2)
with col1:
    st.button("🎤 Press to Talk", on_click=handle_voice_button, disabled=st.session_state.ai_speaking)
with col2:
    st.button("⏹️ Stop AI", on_click=handle_stop_button)

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
    st.rerun()