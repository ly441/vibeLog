from dotenv import load_dotenv
from pathlib import Path
import os
import base64
import requests
from datetime import datetime, timedelta

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class SpotifyService:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

        print("SPOTIFY_CLIENT_ID =", self.client_id)
        print("SPOTIFY_CLIENT_SECRET =", self.client_secret)

        self.access_token = None
        self.token_expiry = None

    def _get_auth_header(self):
        if not self.access_token or datetime.now() > self.token_expiry:
            self._request_token()
        return {'Authorization': f'Bearer {self.access_token}'}

    def _request_token(self):
        auth_str = f"{self.client_id}:{self.client_secret}"
        auth_b64 = base64.b64encode(auth_str.encode()).decode()

        headers = {
            'Authorization': f'Basic {auth_b64}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {'grant_type': 'client_credentials'}

        response = requests.post(
            'https://accounts.spotify.com/api/token',
            headers=headers,
            data=data
        )
        response.raise_for_status()

        token_data = response.json()
        self.access_token = token_data['access_token']
        self.token_expiry = datetime.now() + timedelta(seconds=token_data['expires_in'])

    def get_track(self, track_id):
        headers = self._get_auth_header()
        response = requests.get(
            f'https://api.spotify.com/v1/tracks/{track_id}',
            headers=headers
        )
        response.raise_for_status()
        return response.json()

    def search_track(self, query):
        headers = self._get_auth_header()
        params = {
            'q': query,
            'type': 'track',
            'limit': 5
        }
        response = requests.get(
            'https://api.spotify.com/v1/search',
            headers=headers,
            params=params
        )
        response.raise_for_status()
        return response.json()['tracks']['items']

    def search_artist(self, name):
        headers = self._get_auth_header()
        params = {
            'q': name,
            'type': 'artist',
            'limit': 1
        }
        response = requests.get(
            'https://api.spotify.com/v1/search',
            headers=headers,
            params=params
        )
        response.raise_for_status()
        artists = response.json().get('artists', {}).get('items', [])
        return artists[0] if artists else None
