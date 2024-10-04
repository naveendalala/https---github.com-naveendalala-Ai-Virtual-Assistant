import datetime
import webbrowser

class CommandProcessor:
    def __init__(self):
        self.commands = {
            "play": self.play_music,
            "open": self.open_website,
            "time": self.get_time,
            "date": self.get_date,
            "search": self.search_google,
            "exit": self.exit_program
        }

    def process(self, command, jarvis):
        command = command.lower().strip()
        for key, func in self.commands.items():
            if key in command:
                return func(command, jarvis)
        jarvis.speak("I'm sorry, I don't understand that command. Could you please repeat?")

    def play_music(self, command, jarvis):
        song_name = command.replace("play", "").strip()
        print(f"Attempting to play: {song_name}")  # Debug print
        jarvis.play_song(song_name)  # Assuming Jarvis class has a play_song method

    def open_website(self, command, jarvis):
        jarvis.website_opener.open(command, jarvis)

    def get_time(self, command, jarvis):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        jarvis.speak(f"The current time is {current_time}")

    def get_date(self, command, jarvis):
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        jarvis.speak(f"Today's date is {current_date}")

    def search_google(self, command, jarvis):
        search_query = command.replace("search", "").strip()
        jarvis.speak(f"Searching for {search_query}")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")

    def exit_program(self, command, jarvis):
        jarvis.speak("Goodbye!")
        jarvis.is_active = False  # Set Jarvis to inactive instead of calling exit()
