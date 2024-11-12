import requests
import os
import base64
import unicodedata
import json
import re
from dotenv import load_dotenv

SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
LYRICS_API_BASE_URL = 'https://api.lyrics.ovh/v1'
ALBUM_ID = '1rpCHilZQkw84A3Y9czvMO'
ARTIST_NAME = "Laufey"

class SpotifyClient:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv('clientID')
        self.client_secret = os.getenv('client_Secret')
        self.token = self._get_access_token()

    def _get_access_token(self):
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = base64.b64encode(auth_string.encode('ascii')).decode('ascii')
        
        headers = {
            'Authorization': f'Basic {auth_bytes}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response = requests.post(
            SPOTIFY_TOKEN_URL,
            headers=headers,
            data={'grant_type': 'client_credentials'}
        )
        
        if response.status_code != 200:
            raise Exception("Authentication failed with Spotify API")
            
        return response.json()['access_token']

    def get_album_tracks(self, album_id):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(
            f'{SPOTIFY_API_BASE_URL}/albums/{album_id}',
            headers=headers
        )
        
        if response.status_code != 200:
            raise Exception("Failed to get album information")
            
        return response.json()

class LyricsProcessor:
    @staticmethod
    def clean_lyrics(lyrics):
        normalized = unicodedata.normalize('NFKD', lyrics)
        cleaned = normalized.encode('ascii', 'ignore').decode('utf-8')
        
        cleaned = cleaned.replace(r'\r\n', '\n').replace(r'\n\n\n\n', '\n\n')
        replacements = {
            r'\bIm\b': "I'm",
            r'\byoure\b': "you're",
            r'\bwrot\b': "wrote",
            r'\bhart\b': "heart",
            r'\bWhats\b': "What's"
        }
        
        for pattern, replacement in replacements.items():
            cleaned = re.sub(pattern, replacement, cleaned)
            
        return cleaned

    @staticmethod
    def get_track_lyrics(artist, track_name):
        url = f"{LYRICS_API_BASE_URL}/{artist}/{track_name}"
        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception(f"Status code: {response.status_code}")
            
        return response.json().get('lyrics', 'Lyrics not found.')

def ensure_directories():
    os.makedirs('./Data/Raw', exist_ok=True)
    os.makedirs('./Data/Processed', exist_ok=True)

def main():
    ensure_directories()
    spotify_client = SpotifyClient()
    lyrics_processor = LyricsProcessor()
    
    album_data = spotify_client.get_album_tracks(ALBUM_ID)
    
    with open('./Data/Raw/album.json', 'w', encoding='utf-8') as json_file:
        json.dump(album_data, json_file, indent=4, ensure_ascii=False)
    
    track_names = [track['name'] for track in album_data['tracks']['items']]
    
    for track_name in track_names:
        try:
            lyrics = lyrics_processor.get_track_lyrics(ARTIST_NAME, track_name)
            cleaned_lyrics = lyrics_processor.clean_lyrics(lyrics)
            
            with open(f'./Data/Processed/{track_name}.json', 'w', encoding='utf-8') as lyrics_file:
                json.dump({"lyrics": cleaned_lyrics}, lyrics_file, indent=4, ensure_ascii=False)
                
        except Exception as e:
            print(f"Failed to retrieve lyrics for {track_name}: {e}")

if __name__ == "__main__":
    main()