import difflib
import pygame
import youtube_dl
from youtubesearchpython import VideosSearch
from musicLibrary import get_music_library

class MusicPlayer:
    def __init__(self):
        self.music_library = get_music_library()
        print(f"Music library loaded with {len(self.music_library)} songs")  # Debug print
        pygame.mixer.init()

    def play(self, song_name, jarvis):
        print(f"Searching for song: {song_name}")  # Debug print
        closest_match = self.find_closest_match(song_name, list(self.music_library.keys()))
        if closest_match:
            print(f"Closest match found: {closest_match}")  # Debug print
            jarvis.speak(f"Playing {closest_match}")
            url = self.music_library[closest_match]
            self.play_from_url(url, jarvis)
        else:
            print(f"No match found in library for: {song_name}")  # Debug print
            jarvis.speak(f"Searching for {song_name} on YouTube")
            self.play_from_youtube(song_name, jarvis)

    def play_from_url(self, url, jarvis):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                url = info['formats'][0]['url']
            
            pygame.mixer.music.load(url)
            pygame.mixer.music.play()
            jarvis.speak("Song is now playing")
        except Exception as e:
            print(f"Error playing song: {e}")
            jarvis.speak("I'm sorry, I couldn't play that song.")

    def play_from_youtube(self, song_name, jarvis):
        try:
            videos_search = VideosSearch(song_name, limit=1)
            results = videos_search.result()

            if not results['result']:
                jarvis.speak("Sorry, I couldn't find that song on YouTube.")
                return

            video = results['result'][0]
            video_url = video['link']
            
            self.play_from_url(video_url, jarvis)
        except Exception as e:
            print(f"Error searching/playing YouTube song: {e}")
            jarvis.speak("I'm sorry, I couldn't play that song from YouTube.")

    @staticmethod
    def find_closest_match(query, options):
        query = query.lower()
        options_lower = [opt.lower() for opt in options]
        matches = difflib.get_close_matches(query, options_lower, n=1, cutoff=0.6)
        if matches:
            index = options_lower.index(matches[0])
            return options[index]
        return None
