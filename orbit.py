import os
import time
import webbrowser
import pyautogui
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
from groq import Groq  # Using the specific Groq library

# ================= CONFIGURATION =================
# 1. PASTE YOUR GROQ API KEY HERE:
GROQ_API_KEY = "YOUR_GROQ_API"

# 2. Choose your model (Llama 3.3 is very smart and fast)
MODEL_NAME = "llama-3.3-70b-versatile" 
# =================================================

# Initialize the Groq Client
client = Groq(api_key=GROQ_API_KEY)

def speak(text):
    """Orbit's Voice"""
    print(f"Orbit: {text}")
    try:
        # 'en' for English. For Hindi use 'hi', Spanish 'es', etc.
        tts = gTTS(text=text, lang='en') 
        tts.save("response.mp3")
        mixer.init()
        mixer.music.load("response.mp3")
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)
        mixer.quit()
        if os.path.exists("response.mp3"):
            os.remove("response.mp3")
    except Exception as e:
        print(f"Audio Error: {e}")

def listen_command():
    """Orbit's Ears"""
    r = sr.Recognizer()
    r.energy_threshold = 300 
    r.dynamic_energy_threshold = True 
    
    with sr.Microphone() as source:
        print("\n[Orbit] Listening...")
        r.adjust_for_ambient_noise(source, duration=0.8)
        try:
            # Orbit waits 7 seconds for you to start speaking
            audio = r.listen(source, timeout=7, phrase_time_limit=5)
            print("[Orbit] Recognizing...")
            query = r.recognize_google(audio)
            print(f"You said: {query}")
            return query.lower()
        except Exception:
            return ""

def execute_system_command(query):
    """Orbit's PC Controls"""
    if "open browser" in query or "google" in query:
        speak("Opening browser.")
        webbrowser.open("https://www.google.com")
        return True
    elif "notepad" in query:
        speak("Opening Notepad.")
        os.system("notepad.exe")
        return True
    elif "volume up" in query:
        pyautogui.press("volumeup")
        return True
    elif "volume down" in query on query:
        pyautogui.press("volumedown")
        return True
    elif "screenshot" in query:
        pyautogui.screenshot("orbit_snap.png")
        speak("Screenshot saved to your folder.")
        return True
    return False

def get_groq_response(user_input):
    """Orbit's Brain (Powered by Groq)"""
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system", 
                    "content": "Your name is Orbit. You are a fast PC assistant. You can speak English, Hindi, Chinese, Russian, Japanese, and Spanish. Keep answers very short."
                },
                {"role": "user", "content": user_input}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"!!! GROQ ERROR: {e}")
        return "I'm having trouble connecting to my Groq brain. Check your API key or balance."

def start_orbit():
    speak("Orbit is online and lightning fast.")
    while True:
        query = listen_command()
        
        if not query:
            continue
        
        # Shutdown commands
        if any(word in query for word in ["stop", "exit", "goodbye", "bye"]):
            speak("Goodbye! Orbit shutting down.")
            break
            
        # 1. Check if user wants to control the PC
        if not execute_system_command(query):
            # 2. If not, use Groq to answer the question
            ai_text = get_groq_response(query)
            speak(ai_text)

if __name__ == "__main__":
    start_orbit()
