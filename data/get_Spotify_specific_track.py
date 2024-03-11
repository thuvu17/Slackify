import requests
import data.get_Spotify_token as get_Spotify_token

# Requesting featured playlists from Spotify
access_token = get_Spotify_token.get_token()
base_url = 'https://api.spotify.com/v1/'

headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}


def get_specific_track(track_id):
    track_id_endpoint = 'tracks/' + track_id
    track_url = ''.join([base_url, track_id_endpoint])
    response = requests.get(track_url, headers=headers)
    track = response.json().get('name')
    print(response.json())
    return track


get_specific_track("11dFghVXANMlKmJXsNCbNl")