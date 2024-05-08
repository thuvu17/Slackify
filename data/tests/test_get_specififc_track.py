import data.get_Spotify_specific_track as get_track
import data.songs as song

VALID_ID = '2qSkIjg1o9h3YT9RAgYN75'


# Test that the get_specific_track function returns a valid Spotify track
def test_get_specific_track_valid():
    track = get_track.get_specific_track(VALID_ID)
    assert track is not None
    assert track == {
        song.NAME: 'Espresso',
        song.ARTIST: 'Sabrina Carpenter',
        song.ALBUM: 'Espresso',
        song.BPM: 103.969,
        song.ENERGY: 0.76,
    }
