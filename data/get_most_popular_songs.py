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


# Retrieve the top 10 most popular songs from a featured playlist on Spotify
def get_most_popular_songs():
    response = requests.get(featured_playlists_url, headers=headers)
    songs = response.json().get('items')
    return songs


# Extract relevant data from a song object obtained from Spotify API response
def get_most_popular_songs_data(song):
    track_id = song.get('track').get('id')
    track_name = song.get('track').get('name')
    track_album = song.get('track').get('album').get('name')
    track_artists = [artist.get('name') for artist in
                     song.get('track').get('artists')]
    return {'id': track_id, 'name': track_name,
            'album': track_album, 'artists': track_artists}
