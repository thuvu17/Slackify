"""
This file will manage interactions with our data store.
"""
import data.get_Spotify_specific_track as spotify_track
import data.songs as songs

new_track_ids = ['7qiZfU4dY1lWllzX7mPBI3', '1fidCEsYlaVE3pHwKCvpFZ',
                 '6fNhZRFEkBfgW39W3wKARJ', '4gbVRS8gloEluzf0GzDOFc']


def push_song_to_db(track_id):
    """
    A function to push data into db
    """
    content = spotify_track.get_specific_track(track_id)
    songs.add_song(content)


def main():
    for track_id in new_track_ids:
        push_song_to_db(track_id)


if __name__ == '__main__':
    main()
