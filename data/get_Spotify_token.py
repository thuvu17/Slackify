import requests
import os
from dotenv import load_dotenv

# Requesting Token from Spotify
load_dotenv()
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
auth_url = 'https://accounts.spotify.com/api/token'
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
}


def get_token():
    auth_response = requests.post(auth_url, data=data)
    token = auth_response.json().get('access_token')
    return token
