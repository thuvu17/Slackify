import requests
import get_Spotify_token

token = get_Spotify_token.get_token()
base_url = 'https://api.spotify.com/v1/'

headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

featured_playlists_endpoint = 'browse/featured-playlists/?limit=50'
featured_playlists_url = ''.join([base_url,featured_playlists_endpoint])


def get_featured_playlist():
    response = requests.get(featured_playlists_url,headers=headers)
    playlists = response.json().get('playlists').get('items')
    return playlists
