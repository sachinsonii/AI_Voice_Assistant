import numpy as np
import pyttsx3
import PIL.Image
import pyautogui
import cv2
import threading
import google.generativeai as genai
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import itertools
import speech_recognition as sr
import time
import os

# Read the API key from file
with open("API.txt", 'r') as API:
    api = API.read()
    API.close()

# Initialize pyttsx3 (text-to-speech engine)
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('rate', 150)  # Set voice rate
engine.setProperty('voice', voices[1].id)  # Female voice

# Initialize Google Gemini AI Model
genai.configure(api_key=api)
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize speech recognition
recognizer = sr.Recognizer()

# File to store permanent memory
PERM_MEMORY_FILE = "permanent_memory.txt"

# Memory system with temporary and permanent memory
class MemorySystem:
    def __init__(self):
        self.temp_memory = ""  # Stores the most recent interaction
        self.perm_memory = self.load_perm_memory()  # Load saved memory

    def update_temp_memory(self, user_input, ai_response):
        """Update temporary memory with the latest interaction."""
        self.temp_memory = f"User: {user_input}\nAI: {ai_response}"

    def add_to_perm_memory(self, content):
        """Add new information to permanent memory."""
        self.perm_memory += f"{content}\n"

    def get_combined_memory(self):
        """Combine permanent and temporary memory for context."""
        return f"[{self.perm_memory.strip()}\n\n{self.temp_memory.strip()}]"

    def summarize_perm_memory(self):
        """Summarize permanent memory into key points."""
        summary_prompt = f"Summarize the following points into a concise list:\n{self.perm_memory}"
        response = model.generate_content(summary_prompt)
        return response.text.strip()

    def load_perm_memory(self):
        """Load saved permanent memory from a file."""
        if os.path.exists(PERM_MEMORY_FILE):
            with open(PERM_MEMORY_FILE, "r") as f:
                return f.read().strip()
        return ""

# Function to capture voice input
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust for ambient noise and record audio
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google Web Speech API
            recognized_text = recognizer.recognize_google(audio)
            print("You said: " + recognized_text)
            return recognized_text
        except sr.UnknownValueError:
            engine.say("Sorry, I could not understand the audio.")
            engine.runAndWait()
            return ""
        except sr.RequestError as e:
            engine.say(f"Could not request results from Google Speech Recognition service; {e}")
            engine.runAndWait()
            return ""

# Function for the voice assistant
def assistant(memory_system):
    while True:
        prompt = listen()
        if prompt == "":
            continue

        # Check if the user wants to store something permanently
        if "remember this" in prompt.lower():
            memory_system.add_to_perm_memory(prompt.replace("remember this", "").strip())
            engine.say("Got it! I will remember this.")
            engine.runAndWait()
            continue

        # Combine memory and prompt for AI
        memory_with_context = memory_system.get_combined_memory()

        if "scan screen" in prompt.lower():
            img = pyautogui.screenshot()
            img.save('image.png')
            engine.say("Analysing Screen")
            image = "image.png"
            file = PIL.Image.open(image)
            response = model.generate_content([f"ans in short \nPast info: {memory_with_context}\n\nPrompt: {prompt}", file])
            ai_response = response.text.replace('*', '')
        elif "scan" in prompt.lower():
            vidObj = cv2.VideoCapture(0)
            for i in range(5):
                ret, img = vidObj.read()
            cv2.imwrite("frame.png", img)
            engine.say("Scan Complete")
            image = "frame.png"
            file = PIL.Image.open(image)
            response = model.generate_content([f"{memory_with_context}\n{prompt}", file])
            ai_response = response.text.replace('*', '')
        elif "quit" in prompt.lower():
            break
        else:
            response = model.generate_content(f"{memory_with_context}\n{prompt}")
            ai_response = response.text.replace('*', '')

        # Speak and display the AI's response
        engine.say(ai_response)
        print("AI: ", ai_response)
        engine.runAndWait()

        # Update temporary memory
        memory_system.update_temp_memory(user_input=prompt, ai_response=ai_response)

# Function to update the plot for the animation
def update(frame, ax, radius):
    ax.clear()
    ax.set_box_aspect([1, 1, 1])
    ax.set_facecolor('black')
    ax.grid(False)
    ax.axis('off')
    a = 0.1
    b = 0.1
    theta = np.linspace(0, frame * 0.1, 1000)
    pulse = 1 + 0.5 * np.sin(frame * 0.1)
    r = (a + b * theta) * pulse
    phi = np.linspace(0, np.pi, len(theta))
    theta = theta % (2 * np.pi)
    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi)
    ax.plot(x, y, z, color="cyan", linewidth=0.1)

# Function to create the 3D spherical spiral animation
def animated_spiral_on_sphere():
    engine.say("Initializing and Booting")
    engine.runAndWait()
    plt.rcParams['toolbar'] = 'None'
    radius = 10
    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111, projection='3d')
    fig.patch.set_facecolor('black')
    ax.view_init(elev=90, azim=90)
    ani = FuncAnimation(fig, update, frames=itertools.count(1, 10), fargs=(ax, radius), interval=50, repeat=True)
    plt.show()

# Main function to start the assistant and animation
def main():
    memory_system = MemorySystem()  # Initialize memory system

    # Start the assistant in a separate thread
    assistant_thread = threading.Thread(target=assistant, args=(memory_system,))
    assistant_thread.daemon = True
    assistant_thread.start()

    # Start the animation
    animated_spiral_on_sphere()

    # Summarize and save memory on exit
    summary = memory_system.summarize_perm_memory()
    print("Session Summary:")
    print(summary)
    """Save permanent memory to a file."""
    with open(PERM_MEMORY_FILE, "w") as f:
        f.write(summary)
        f.write("\n")

if __name__ == "__main__":
    main()
