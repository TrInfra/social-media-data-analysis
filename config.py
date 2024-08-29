import spotipy
from dotenv import load_dotenv
import os
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

clientID = os.getenv('clientID')
client_Secret = os.getenv('client_Secret')
redirect_url = os.getenv('redirect_url')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= clientID,
                                               client_secret=client_Secret,
                                               redirect_uri=redirect_url,
                                               scope="user-library-read"))
print(sp)