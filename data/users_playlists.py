# """
# users_playlists.py: the interface to our user-playlist interaction data.
# """
# import random
# from bson import ObjectId

# import data.db_connect as dbc
# import playlists as playlists

# USERS_PLAYLISTS_COLLECT = 'users_playlists'

# MONGO_ID = '_id'
# USER_ID = 'user_id'
# PLAYLIST_ID = 'playlist_id'

# MIN_NAME_LEN = 1

# BIG_NUM = 100000000000000


# # Return random playlist id
# def _get_test_pname():
#     name = 'playlist'
#     rand_part = random.randint(0, BIG_NUM)
#     return name + str(rand_part)


# # Return random user id
# def _get_test_uid():
#     return str(ObjectId())


# def _get_test_pid(_id: str):
#     dbc.connect_db()
#     pid = dbc.fetch_one(USERS_PLAYLISTS_COLLECT,
#                         {MONGO_ID: ObjectId(_id)})
#     return str(pid[PLAYLIST_ID])


# # Take in the user email and name of a playlist that you want to find in DB
# # Return true if given playlist is found, else return false
# def already_exist(user_id: str, playlist_id: str) -> bool:
#     dbc.connect_db()
#     user_id = ObjectId(user_id)
#     playlist_id = ObjectId(playlist_id)
#     print(f'already uid {type(user_id)}: {user_id}')
#     print(f'already pid {type(playlist_id)}: {playlist_id}')
#     return dbc.fetch_one(USERS_PLAYLISTS_COLLECT, {USER_ID: user_id,
#                          PLAYLIST_ID: playlist_id}) is not None


# # Take in the user email and name of a playlist that you want to find in DB
# # Return the associated playlist if it exists, None if not
# def get_playlist(user_id: str, playlist_id: str) -> dict:
#     if already_exist(user_id, playlist_id):
#         return playlists.get_playlist(PLAYLIST_ID)


# # def get_playlists(user_id: str):
# #     """
# #     Our contract:
# #     - No arguments.
# #     - Returns a list of playlist names keyed on playlist email (a str).
# #     - Each playlist email must be the key for a dictionary.
# #     - That dictionary must at least include a EMAIL member that is a string
# #     value.
# #     """
# #     dbc.connect_db()
# #     playlist_ids = dbc.fetch_all_as_list(USERS_PLAYLISTS_COLLECT,
# #                                          {USER_ID: user_id}, PLAYLIST_ID)
# #     playlists_fetched = {}
# #     for playlist_id in playlist_ids:
# #         this_playlist = playlists.get_playlist(playlist_id)
# #         playlists_fetched[this_playlist[playlists.MONGO_ID]] =
# #                                  this_playlist
# #     return playlists_fetched


# def add_playlist(user_id: str, playlist_name: str) -> bool:
#     # Check if a playlist with same email + name
#     # is already in the database
#     if len(playlist_name) < MIN_NAME_LEN:
#         raise ValueError("Minimum playlist name length is 1 character!")
#     # ensure user email is valid
#     # can be deleted in the future since user email must be valid here
#     else:
#         playlist_added = playlists.add_playlist(playlist_name)
#         if playlist_added.acknowledged:
#             playlist_id = playlist_added.inserted_id
#             print(f'add uid {type(user_id)}: {user_id}')
#             print(f'add pid {type(playlist_id)}: {playlist_id}')
#             user_playlist_data = {USER_ID: ObjectId(user_id),
#                                   PLAYLIST_ID: playlist_id}
#             dbc.connect_db()
#             _id = dbc.insert_one(USERS_PLAYLISTS_COLLECT, user_playlist_data)
#             return _id


# def del_playlist(user_id: str, playlist_id: str):
#     if not already_exist(user_id, playlist_id):
#         raise ValueError(f"Delete Fail: Playlist with id {playlist_id} "
#                          "not in database")
#     return dbc.del_one(USERS_PLAYLISTS_COLLECT, {USER_ID: user_id,
#                        PLAYLIST_ID: playlist_id})


# # def update_playlist_name(user_id: str, playlist_id: str,
# #                          new_playlist_name: str) -> bool:
# #     if not already_exist(user_id, playlist_id):
# #         raise ValueError("Update failure: the playlist is not in
# #                          database.")
# #     playlist = playlists.get_playlist(playlist_id)
# #     if new_playlist_name == playlist[playlists.NAME]:
# #         raise ValueError("A playlist with the same name already existed!")
