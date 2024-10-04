import webbrowser

class WebsiteOpener:
    def __init__(self):
        self.websites = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "spotify": "https://www.spotify.com",
            "netflix": "https://www.netflix.com",
            "amazon": "https://www.amazon.com",
            "facebook": "https://www.facebook.com",
            "instagram": "https://www.instagram.com",
            "twitter": "https://www.twitter.com",
            "linkedin": "https://www.linkedin.com",
            "github": "https://www.github.com",
            "stackoverflow": "https://www.stackoverflow.com",
            "wikipedia": "https://www.wikipedia.org",
            "imdb": "https://www.imdb.com",
            "reddit": "https://www.reddit.com",
            "quora": "https://www.quora.com",
            "medium": "https://www.medium.com",
            "pinterest": "https://www.pinterest.com",
            "tumblr": "https://www.tumblr.com",
            "twitch": "https://www.twitch.tv",
            "vimeo": "https://www.vimeo.com",
            "soundcloud": "https://www.soundcloud.com",
            "tiktok": "https://www.tiktok.com",
            "snapchat": "https://www.snapchat.com",
            "whatsapp": "https://web.whatsapp.com",
            "telegram": "https://web.telegram.org",
            "discord": "https://discord.com",
            "slack": "https://slack.com",
            "zoom": "https://zoom.us",
            "microsoft teams": "https://teams.microsoft.com",
            "google meet": "https://meet.google.com",
            "trello": "https://trello.com",
            "asana": "https://app.asana.com",
            "jira": "https://www.atlassian.com/software/jira",
            "notion": "https://www.notion.so",
            "evernote": "https://www.evernote.com",
            "dropbox": "https://www.dropbox.com",
            "google drive": "https://drive.google.com",
            "onedrive": "https://onedrive.live.com",
            "box": "https://www.box.com",
            "coursera": "https://www.coursera.org",
            "udemy": "https://www.udemy.com",
            "edx": "https://www.edx.org",
            "khan academy": "https://www.khanacademy.org",
            "duolingo": "https://www.duolingo.com",
        }

    def open(self, command, jarvis):
        site = next((site for site in self.websites if site in command.lower()), None)
        if site:
            jarvis.speak(f"Opening {site}")
            webbrowser.open(self.websites[site])
        else:
            jarvis.speak("Sorry, I don't know how to open that website.")
