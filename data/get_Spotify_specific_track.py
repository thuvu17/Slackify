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
    featured_playlists_url = ''.join([base_url, track_id_endpoint])
    response = requests.get(featured_playlists_url, headers=headers)
    track = response.json().get('name')
    return track
