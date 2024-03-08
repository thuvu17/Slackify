# """
# users_playlists.py: the interface to our user-playlist interaction data.
# """
# from bson import ObjectId

# import data.db_connect as dbc
# # import playlists as playlists

# USERS_PLAYLISTS_COLLECT = 'users_playlists'

# MONGO_ID = '_id'
# USER_ID = 'user_id'
# PLAYLIST_ID = 'playlist_id'

# MIN_NAME_LEN = 1

# BIG_NUM = 100000000000000


# # Return random user id
# def _get_test_uid():
#     return str(ObjectId())


# # Return random user id
# def _get_test_pid():
#     return str(ObjectId())


# def _get_test_schema():
#     user_id = _get_test_uid()
#     playlist_id = _get_test_pid()
#     return {USER_ID: user_id, PLAYLIST_ID: playlist_id}


# # def _get_inserted_test_pid(_id: str):
# #     dbc.connect_db()
# #     pid = dbc.fetch_one(USERS_PLAYLISTS_COLLECT,
# #                         {MONGO_ID: ObjectId(_id)})
# #     return str(pid[PLAYLIST_ID])


# # Take in the user email and name of a playlist that you want to find in DB
# # Return true if given playlist is found, else return false
# def already_exist(user_id: str, playlist_id: str) -> bool:
#     dbc.connect_db()
#     print(f'already uid {type(user_id)}: {user_id}')
#     print(f'already pid {type(playlist_id)}: {playlist_id}')
#     return dbc.fetch_one(USERS_PLAYLISTS_COLLECT,
#                          {USER_ID: ObjectId(user_id),
#                          PLAYLIST_ID: ObjectId(playlist_id)}) is not None


# # # Take in the user email and name of a playlist that you want to find in DB
# # # Return the associated playlist if it exists, None if not
# # def get_playlists(user_id: str) -> dict:
# #     dbc.connect_db()
# #     return dbc.fetch_all_as_list(USERS_PLAYLISTS_COLLECT,
# # {USER_ID: user_id},
# #                                  PLAYLIST_ID)


# def get_playlist_ids_as_list(user_id: str):
#     dbc.connect_db()
#     playlist_ids = dbc.fetch_all_as_list(USERS_PLAYLISTS_COLLECT,
#                                          {USER_ID: ObjectId(user_id)},
#                                          PLAYLIST_ID)
#     return playlist_ids


# def add_playlist(user_id: str, playlist_id: str) -> bool:
#     if playlist_id:
#         user_playlist_data = {USER_ID: ObjectId(user_id),
#                               PLAYLIST_ID: ObjectId(playlist_id)}
#         dbc.connect_db()
#         _id = dbc.insert_one(USERS_PLAYLISTS_COLLECT, user_playlist_data)
#         return _id is not None


# def del_playlist(user_id: str, playlist_id: str):
#     if not already_exist(user_id, playlist_id):
#         raise ValueError(f"Delete Fail: Playlist with id {playlist_id} "
#                          "not in database")
#     return dbc.del_one(USERS_PLAYLISTS_COLLECT, {USER_ID: ObjectId(user_id),
#                        PLAYLIST_ID: ObjectId(playlist_id)})


# # def update_playlist_name(user_id: str, playlist_id: str,
# #                          new_playlist_name: str) -> bool:
# #     if not already_exist(user_id, playlist_id):
# #         raise ValueError("Update failure: the playlist is not in
# #                          database.")
# #     playlist = playlists.get_playlist(playlist_id)
# #     if new_playlist_name == playlist[playlists.NAME]:
# #         raise ValueError("A playlist with the same name already existed!")
