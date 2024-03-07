# """
# playlists_songs.py: the interface to our playlist-song interaction data.
# """
# import data.db_connect as dbc


# def song_exists_in_playlist(user_email: str, playlist_name: str,
#                             song_id: str) -> bool:
#     playlist = get_playlist(user_email, playlist_name)
#     return song_id in playlist.get(SONGS)


# def update_add_songs_in_playlist(user_email: str, playlist_name: str,
#                                  song_id: str) -> bool:
#     if not already_exist(user_email, playlist_name):
#         raise ValueError(f"Failed to add a song: {playlist_name}"
#                          "not in database.")
#     elif song_exists_in_playlist(user_email, playlist_name, song_id):
#         raise ValueError("Failed to add a song: the song"
#                          "is already in the playlist.")
#     else:
#         playlist = get_playlist(user_email, playlist_name)
#         songs_in = playlist[SONGS]
#         print(songs_in)
#         songs_in.append(song_id)
#         print(songs_in)
#         dbc.connect_db()
#         return dbc.update_doc(PLAYLISTS_COLLECT, {EMAIL: user_email,
#                               NAME: playlist_name}, {SONGS: songs_in})
