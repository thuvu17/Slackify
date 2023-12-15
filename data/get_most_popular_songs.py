import requests
import data.get_Spotify_token as get_Spotify_token

# Get top 10 most listened songs on Spotify

access_token = get_Spotify_token.get_token()
base_url = 'https://api.spotify.com/v1/'

headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

featured_playlists_endpoint = \
    'playlists/2YRe7HRKNRvXdJBp9nXFza/tracks?offset=0&limit=10'
featured_playlists_url = ''.join([base_url, featured_playlists_endpoint])


def get_most_popular_songs():
    response = requests.get(featured_playlists_url, headers=headers)
    songs = response.json().get('items')
    return songs
