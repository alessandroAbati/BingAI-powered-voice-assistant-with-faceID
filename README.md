# BingAI-Powered Voice Assistant

This repository contains code for a BingAI-powered voice assistant that can recognize users through face detection login and interact with them, providing information from BingAI responses.

## Features

The provided Python script implements an interactive voice-based AI assistant that integrates speech recognition, text-to-speech synthesis, face recognition, and AI conversation capabilities. This comprehensive script allows users to interact with the AI assistant through voice commands, receiving spoken responses, and performing actions based on user inputs.

### 1. Voice Interaction

The AI assistant utilizes the `speech_recognition` library to listen for user commands through the microphone. Users can initiate interactions by speaking prompts and questions to the assistant.

### 2. Text-to-Speech Synthesis

The script employs the Amazon Polly service to synthesize spoken responses from text. The `PollySynthesizer` class handles this functionality, providing a seamless conversion of AI-generated text responses into natural-sounding speech.

### 3. Face Recognition and Authentication

The `FaceLogin` class enables user authentication through facial recognition. Users can enroll by capturing their facial features, which are then stored as templates for future recognition. This feature enhances security and personalization by allowing the assistant to recognize registered users based on their unique facial characteristics.
New users can easily enroll in the system through the facial recognition feature. The script guides users through the process of capturing facial images, creating an average face template, and saving it for later recognition. This feature enhances the assistant's ability to personalize interactions.

### 4. AI Chatbot Integration

The AI assistant interacts with an external AI chatbot through the Bing chatbot API. The `AIAssistant` class handles the communication with the chatbot, sending user prompts, and receiving text responses. This integration enables the assistant to provide relevant and contextually appropriate answers to user queries. The `EdgeGPT` library is employed to interact with the chatbot, and the conversation style is set to `precise` to ensure accurate and coherent replies. The AI assistant provides a seamless and user-friendly experience through spoken prompts, text-to-speech responses, and user-friendly interactions. It enables a natural and intuitive way for users to interact with technology.

### 5. Error Handling and Stability

The script includes error handling mechanisms to manage potential exceptions during various stages of execution. This ensures that users are provided with informative messages in case of errors or failures.

### 6. Easily Extensible

Developers can extend the functionality of the AI assistant by integrating additional features, modifying the conversation with the chatbot, or enhancing the face recognition process. The script's modular structure allows for easy expansion and customization.

## Requirements

To use this voice assistant, you need to fulfill the following requirements:

1. **Python 3.x**: Make sure you have Python installed on your system.

2. **AWS Account and Polly Access**: The voice synthesis feature is powered by Amazon Polly. You need an AWS account and API credentials for Polly to use this feature.

## Getting Started

### Using Conda (Recommended)

1. Clone the repository:

   ```bash
   git clone https://github.com/alessandroAbati/AI-powered-voice-assistant.git
   cd AI-powered-voice-assistant

2. Set up virtual environment with Conda using the provided environment.yml file:

   ```bash
   conda env create -f environment.yml
   conda activate voice-assistant-env

3. Set up environment variables for Amazon AWS services.
   
4. Run the voice assistant:
   ```bash
   python main.py

### Using Pip

1. Clone the repository:

   ```bash
   git clone https://github.com/alessandroAbati/AI-powered-voice-assistant.git
   cd AI-powered-voice-assistant

2. Set up a virtual environment (optional but recommended)::

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: .\venv\Scripts\activate

3. Install the required packages using pip:
   
   ```bash
   pip install -r requirements.txt

4. Set up environment variables for Amazon AWS services.
   
5. Run the voice assistant:
   ```bash
   python main.py

## License

This script is provided under the [MIT License](LICENSE), allowing you to freely use and modify the code according to your needs. See the LICENSE file for more details.

## Acknowledgments

This project was developed using various open-source libraries and technologies. We acknowledge the contributions of the developers and maintainers of these libraries, which have made this AI assistant possible.

## Next Steps/ Future Improvements
Here are some potential areas for enhancement and development:

- **Handle long conversation**: Implement features to handle long conversation with the AI using more than one prompt.

- **Error Handling**: Implement robust error handling to gracefully handle API errors or unexpected user input.

- **Optimization**: Optimize the code for efficiency and performance, especially when interacting with external APIs.

- **Continuous Learning**: Explore methods to make the voice assistant learn from user interactions and improve over time.

- **Community Contributions**: Encourage others to contribute to the project by adding new features, fixing bugs, or improving documentation.

- **User Interface**: Create a graphical user interface (GUI) to make the voice assistant more user-friendly.

Feel free to contribute to this project by addressing any of the above points or by suggesting your own ideas!
