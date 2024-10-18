import requests
import os
import base64
import unicodedata
import json
import re
from dotenv import load_dotenv

load_dotenv()

clientID = os.getenv('clientID')
client_Secret = os.getenv('client_Secret')

# Authentication conversion to base 64
string = f"{clientID}:{client_Secret}"
string_byte = string.encode('ascii')

base64_bytes = base64.b64encode(string_byte)
base64_string = base64_bytes.decode('ascii')

# Request access token
url = 'https://accounts.spotify.com/api/token'

headers = {
    'Authorization': f'Basic {base64_string}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

payload = {'grant_type': 'client_credentials'}

response = requests.post(url=url, headers=headers, data=payload)

token = response.json()['access_token']

id_album = '1rpCHilZQkw84A3Y9czvMO'

# Request artist
url = f'https://api.spotify.com/v1/albums/{id_album}'

headers = {'Authorization': f'Bearer {token}'}

response = requests.get(url=url, headers=headers)
data = response.json()

if response.status_code == 200:
    with open('./Data/Raw/album.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

track_names = [track['name'] for track in data['tracks']['items']]

def clean_lyrics(lyrics):
    normalized = unicodedata.normalize('NFKD', lyrics)
    cleaned = normalized.encode('ascii', 'ignore').decode('utf-8')
    
    cleaned = cleaned.replace(r'\r\n', '\n').replace(r'\n\n\n\n', '\n\n')
    cleaned = re.sub(r'\bIm\b', "I'm", cleaned)
    cleaned = re.sub(r'\byoure\b', "you're", cleaned)
    cleaned = re.sub(r'\bwrot\b', "wrote", cleaned)
    cleaned = re.sub(r'\bhart\b', "heart", cleaned)
    cleaned = re.sub(r'\bWhats\b', "What's", cleaned)

    return cleaned

artist = "Laufey"
for track_name in track_names:
    url_lyrics = f"https://api.lyrics.ovh/v1/{artist}/{track_name}"
    try:
        response_lyrics = requests.get(url_lyrics)
        if response_lyrics.status_code == 200:
            lyrics_data = response_lyrics.json()
            cleaned_lyrics = clean_lyrics(lyrics_data.get('lyrics', 'Lyrics not found.'))

            with open(f'./Data/Processed/{track_name}.json', 'w', encoding='utf-8') as lyrics_file:
                json.dump({"lyrics": cleaned_lyrics}, lyrics_file, indent=4, ensure_ascii=False)
        else:
            print(f"Failed to retrieve lyrics for {track_name}: {response_lyrics.status_code}")
    except Exception as e:
        print(f"Failed to retrieve lyrics for {track_name}: {e}")