import requests
import json
import data.get_Spotify_token as get_Spotify_token
import data.songs as song

# Requesting featured playlists from Spotify
access_token = get_Spotify_token.get_token()
base_url = 'https://api.spotify.com/v1/'

headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}


def get_specific_track(track_id):
    track_id_endpoint = 'tracks/' + track_id
    feature_endpoint = 'audio-features/' + track_id
    info_url = ''.join([base_url, track_id_endpoint])
    feature_url = ''.join([base_url, feature_endpoint])

    info = requests.get(info_url, headers=headers).json()
    audio_feature = requests.get(feature_url, headers=headers).json()
    print('Song info:', json.dumps(info, indent=2))
    print('===========================')
    print('Song audio feature:', json.dumps(audio_feature, indent=2))

    song_name = info.get('name')
    artist = info.get('artists')[0]['name']
    album_name = info.get('album')['name']
    bpm = audio_feature.get('tempo')
    energy = audio_feature.get('energy')
    track = {
        song.NAME: song_name,
        song.ARTIST: artist,
        song.ALBUM: album_name,
        song.BPM: bpm,
        song.ENERGY: energy,
    }
    return track


get_specific_track("11dFghVXANMlKmJXsNCbNl")
