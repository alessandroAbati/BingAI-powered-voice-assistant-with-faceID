# Import necessary libraries
import openai
import asyncio
import re
import boto3
import pydub
from pydub import playback
import speech_recognition as sr
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import numpy as np
import platform
from pywhispercpp.model import Model
import browser_cookie3
import cv2
import face_recognition
import os
import time

# Util functions
def get_cookies(url): # Function to handle cookies
    # List of supported browsers
    browsers = [
        browser_cookie3.edge,
    ]
    for browser_fn in browsers:
        try:
            cookies = []
            cj = browser_fn(domain_name=url)
            for cookie in cj:
                cookies.append(cookie.__dict__)
            return cookies
        except:
            continue

def play_audio(audio_data): # Function to reproduce the audio
    # Convert the audio data to numpy array and calculate required padding
    audio = np.frombuffer(audio_data, dtype=np.int16)
    sample_width = 2  # Assuming 16-bit audio
    channels = 1  # Mono audio
    padding = (len(audio) % (sample_width * channels))
    if padding > 0:
        padding = (sample_width * channels) - padding
        audio = np.pad(audio, (0, padding), mode='constant')

    playback.play(pydub.AudioSegment(
        data=audio.tobytes(),
        sample_width=sample_width,
        frame_rate=16000,
        channels=channels
    ))

# Class to manage ASR
class ASR:
    def __init__(self, model):
        self.model = model

    def transcribe(self, audio_data):
        try:
            result = self.model.transcribe(media=audio_data.flatten(), suppress_non_speech_tokens=True, single_segment = True)
            phrase = ""
            for segment in result:
                phrase += segment.text
            return phrase
        except Exception as e:
            print("Error transcribing audio:", e)
            return None

# Class to handle voice synthesis using Amazon Polly
class PollySynthesizer:
    def __init__(self):
        self.polly = boto3.client('polly', region_name='eu-west-2')

    def synthesize_speech(self, text):
        response = self.polly.synthesize_speech(
            Text=text,
            OutputFormat='pcm',
            VoiceId='Arthur',
            Engine='neural'
        )

        audio_data = response['AudioStream'].read()
        return audio_data
    
class Listener:
    def __init__(self):
        # Initialize necessary components for listening to the user
        self.recognizer = sr.Recognizer()  # Speech recognizer instance
        self.asr = ASR(Model('tiny.en'))  # ASR instance to transcribe audio using whisper model

    def listen_for_user_input(self):
        print("Speak a prompt...")
        with sr.Microphone(sample_rate=16000) as source:
            try:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=30)  # Set a timeout for listening
                audio = audio.get_wav_data()
                audio_data = (np.frombuffer(audio, dtype=np.int16).astype(np.float32)) / (2 ** 15)
                user_input = self.asr.transcribe(audio_data)
                print(f"You said: {user_input}")
                return user_input
            except sr.WaitTimeoutError:
                print("Listening timeout. No user input detected.")
                return None
            except Exception as e:
                print("Error occurred during user input processing:", e)
                return None
    
class FaceLogin:
    def __init__(self, synthesizer, listener):
        # Initialize the list of registered users by reading templates from files
        self.registered_users = [file.split("_")[0] for file in os.listdir("User_templates")]
        self.synthesizer = synthesizer # Initialise the synthesizer
        self.listener = listener # Initialise the listener class

    def load_registered_user_template(self, user_name):
        # Load a registered user's face template from file
        if os.path.exists(f"User_templates/{user_name}_template.npy"):
            template = np.load(f"User_templates/{user_name}_template.npy")
            return template
        else:
            return None

    def save_registered_user_template(self, encoding, user_name):
        # Save a registered user's face template to file
        np.save(f"User_templates/{user_name}_template.npy", encoding)

    def create_enrolled_template(self, camera, num_samples=10):
        # Capture multiple images for enrollment and create an average face template
        play_audio(self.synthesizer.synthesize_speech("Capturing images for enrollment. Please look at the camera."))
        face_encodings = []

        while len(face_encodings) < num_samples:
            ret, frame = camera.read()
            face_locations = face_recognition.face_locations(frame)
            if len(face_locations) == 1:
                encoding = face_recognition.face_encodings(frame, face_locations)[0]
                face_encodings.append(encoding)

        enrolled_template = np.mean(face_encodings, axis=0)
        return enrolled_template

    def ask_username(self):
        # Prompt the user for their preferred username
        play_audio(self.synthesizer.synthesize_speech("How would you like to be called?"))
        user_name = self.listener.listen_for_user_input()
        return ''.join(e for e in user_name if e.isalnum())

    def enroll_user(self):
        # Enroll a new user by capturing their face template
        video_capture = cv2.VideoCapture(0)
        enrolled_template = self.create_enrolled_template(video_capture)
        video_capture.release()
        cv2.destroyAllWindows()

        user_name = self.ask_username()

        self.save_registered_user_template(enrolled_template, user_name)
        play_audio(self.synthesizer.synthesize_speech(f"User ({user_name}) registred successfully."))

    def welcome(self, user_name):
        # Display a welcome message for the recognized user
        play_audio(self.synthesizer.synthesize_speech(f"Welcome, {user_name}!"))

    def ask_to_enroll(self, message):
        # Ask the user if they want to enroll and initiate enrollment if needed
        play_audio(self.synthesizer.synthesize_speech(f"{message}"))
        ans = ''.join(c for c in self.listener.listen_for_user_input() if c.isalpha())
        if "yes" in ans.lower():
            self.enroll_user()
            return True
        else:
            return False

    def recognize_users(self):
        # Main function to manage user recognition and enrollment
        self.registered_users = [file.split("_")[0] for file in os.listdir("User_templates")]
        if not self.registered_users:
            self.ask_to_enroll("No registered user template found. Do you want to be registred as an user?")
            self.registered_users = [file.split("_")[0] for file in os.listdir("User_templates")]

        # Recognize users based on their face templates
        for user in self.registered_users:
            registered_user_template = self.load_registered_user_template(user)

            video_capture = cv2.VideoCapture(0)

            t_end = time.time() + 5
            while True:
                if time.time() > t_end:
                    break
                ret, frame = video_capture.read()
                face_locations = face_recognition.face_locations(frame)
                face_encodings = face_recognition.face_encodings(frame, face_locations)

                for face_encoding in face_encodings:
                    if registered_user_template is not None:
                        matches = face_recognition.compare_faces([registered_user_template], face_encoding)
                        if any(matches):
                            self.welcome(user)
                            video_capture.release()
                            cv2.destroyAllWindows()
                            return True

            video_capture.release()
            cv2.destroyAllWindows()

        if self.ask_to_enroll("No matches detected with current users. Do you want to be registred as a new user?"):
            if self.recognize_users():
                return True
        else:
            return False

class AIAssistant:
    def __init__(self, synthesizer, listener):
        # Initialize necessary components for the AI assistant
        self.cookies = get_cookies('.bing.com')  # Get browser cookies for authentication
        self.synthesizer = synthesizer  # Initialise synthesizer for text-to-speech using PollySynthesizer
        self.listener = listener # Initialise listener class

    async def handle_bing_assistant(self, user_input):
        bot = Chatbot(cookies=self.cookies)
        #print(f"\n\n{bot.get_activity()}\n\n")
        response = await bot.ask(prompt=user_input, conversation_style=ConversationStyle.precise)
        # Select only the bot response from the response dictionary
        for message in response["item"]["messages"]:
            if message["author"] == "bot" and 'messageType' not in message: # Makes sure that we get the AI correct answer from the response
                bot_response = message["text"]            
        # Remove [^#^] citations in response
        bot_response = re.sub(r'\[\^\d+\^\]', '', bot_response)
        #return "Sorry. Something went wrong."
        await bot.close()
        return bot_response

    async def run(self):
        while True:
            synthesize_speech_data = self.synthesizer.synthesize_speech('What can I help you with?')
            play_audio(synthesize_speech_data)

            user_input = self.listener.listen_for_user_input()  # Listen for user input

            bot_response = await self.handle_bing_assistant(user_input)

            print("Bot's response:", bot_response)
            synthesize_bot_response_data = self.synthesizer.synthesize_speech(bot_response)
            play_audio(synthesize_bot_response_data)
            time.sleep(1)

# Initialize and run the voice assistant
if __name__ == "__main__":
    synthesizer = PollySynthesizer()
    listener = Listener()
    face_login = FaceLogin(synthesizer, listener)
    if face_login.recognize_users():
        voice_assistant = AIAssistant(synthesizer, listener)
        asyncio.run(voice_assistant.run())
    else:
        play_audio(synthesizer.synthesize_speech("Access denied!"))
