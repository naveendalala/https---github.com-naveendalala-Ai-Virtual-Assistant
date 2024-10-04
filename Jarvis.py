import speech_recognition as sr
import pyttsx3
import os
import logging
from youtubesearchpython import VideosSearch
import pygame
import urllib.request
import threading

# Assuming these classes are defined in separate files in the same directory
from CommandProcessor import CommandProcessor
from MusicPlayer import MusicPlayer
from WebsiteOpener import WebsiteOpener

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Jarvis:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = self.setup_tts_engine()
        self.command_processor = CommandProcessor()
        self.music_player = MusicPlayer()
        self.website_opener = WebsiteOpener()
        self.is_active = True
        pygame.mixer.init()

    @staticmethod
    def setup_tts_engine():
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        return engine

    def speak(self, text):
        logging.info(f"Jarvis: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_for_command(self):
        try:
            with sr.Microphone() as source:
                logging.info("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)

            command = self.recognizer.recognize_google(audio, language='en-US').lower()
            logging.info(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            logging.warning("Speech was unintelligible")
            self.speak("Sorry, I didn't catch that. Could you please repeat?")
        except sr.RequestError as e:
            logging.error(f"Could not request results from Google Speech Recognition service; {e}")
            self.speak("I'm having trouble connecting to the speech recognition service.")
        except sr.WaitTimeoutError:
            logging.warning("Listening timed out. No speech detected.")
            self.speak("I didn't hear anything. Please try again.")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            self.speak("An unexpected error occurred. Please try again.")
        return None

    def play_song(self, song_name):
        self.speak(f"Searching for {song_name}")
        try:
            # Search for the song on YouTube
            videos_search = VideosSearch(song_name, limit=1)
            results = videos_search.result()

            if not results['result']:
                self.speak("Sorry, I couldn't find that song.")
                return

            video = results['result'][0]
            video_url = video['link']
            
            # Use youtube-dl to get the audio stream URL
            import youtube_dl
            ydl_opts = {'format': 'bestaudio/best'}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                url = info['formats'][0]['url']

            # Play the audio using pygame
            pygame.mixer.music.load(url)
            pygame.mixer.music.play()
            
            self.speak(f"Now playing {video['title']}")
        except Exception as e:
            logging.error(f"An error occurred while playing the song: {str(e)}")
            self.speak("I'm sorry, I couldn't play that song.")

    def run(self):
        self.speak("Initializing Jarvis")
        self.speak("I'm ready for your commands, Boss!")

        while self.is_active:
            command = self.listen_for_command()
            if command:
                if "exit" in command:
                    self.speak("Goodbye, Boss! Have a great day!")
                    self.is_active = False
                elif command.startswith("play"):
                    song_name = command.replace("play", "").strip()
                    self.play_song(song_name)
                else:
                    try:
                        self.command_processor.process(command, self)
                    except Exception as e:
                        logging.error(f"Error processing command: {str(e)}")
                        self.speak("I encountered an error while processing your command.")

def main():
    logging.info(f"Current working directory: {os.getcwd()}")
    logging.info(f"Files in the current directory: {os.listdir()}")

    jarvis = Jarvis()
    try:
        jarvis.run()
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received. Shutting down.")
        jarvis.speak("Shutting down due to keyboard interrupt. Goodbye!")

if __name__ == "__main__":
    main()
