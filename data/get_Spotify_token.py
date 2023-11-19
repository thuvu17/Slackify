import requests

# Requesting Token from Spotify
client_id = '7641947490644dc6a87899c4e8878443'
client_secret = '91e7d14c7c73474a838497faeaae3723'
auth_url = 'https://accounts.spotify.com/api/token'
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
}


def get_token():
    auth_response = requests.post(auth_url, data=data)
    access_token = auth_response.json().get('access_token')
    return access_token
