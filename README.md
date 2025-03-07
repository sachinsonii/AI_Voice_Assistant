# AI Voice Assistant

This AI-powered voice assistant integrates speech recognition, text-to-speech synthesis, computer vision, and Google Gemini AI to create an interactive assistant with memory and learning capabilities.

## Features
- **Voice Recognition**: Uses speech recognition to process voice commands.
- **AI-Powered Responses**: Leverages Google Gemini AI to generate responses based on past interactions.
- **Memory System**: Retains temporary and permanent memory to improve contextual understanding.
- **Screen and Camera Scanning**: Can analyze screenshots or camera images for contextual AI processing.
- **Text-to-Speech (TTS)**: Provides spoken responses using pyttsx3.
- **3D Animated Visualization**: Displays an animated spiral sphere while the assistant is running.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Required libraries:
  ```sh
  pip install numpy pyttsx3 pillow pyautogui opencv-python matplotlib speechrecognition google-generativeai
  ```
- Google Gemini API key (stored in `API.txt`).

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/sachinsonii/AI_Voice_Assistant.git
   cd AI_Voice_Assistant
   ```
2. Place your **Google Gemini API Key** inside a text file named `API.txt`.
3. Run the assistant:
   ```sh
   python main.py
   ```

## Usage
- The assistant listens for voice commands automatically.
- Commands like `remember this` will store information permanently.
- Say **"scan screen"** to capture and analyze the screen.
- Say **"scan"** to capture and analyze an image using the camera.
- Say **"quit"** to exit the assistant.

## Memory System
- **Temporary Memory**: Stores the most recent conversation.
- **Permanent Memory**: Stores user-defined facts in `permanent_memory.txt`.
- The assistant uses both memory types to provide better contextual responses.

## Future Improvements
- Enhance neural network memory for improved learning.
- Add more advanced AI models.
- Improve speech synthesis for more natural responses.
- Implement GUI-based controls.

## License
This project is licensed under the MIT License.

