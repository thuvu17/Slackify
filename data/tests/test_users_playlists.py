# import pytest
# from bson import ObjectId

# import data.users_playlists as upls

# # Yield a temporary user-playlist for testing
# # @pytest.fixture(scope='function')
# # def temp_playlist():
# #     pid = upls._get_test_pid()
# #     uid = upls._get_test_uid()
# #     playlist = upls.get_test_playlist()
# #     ret = pls.add_playlist(playlist['name'])
# #     playlist[pls.MONGO_ID] = ret.inserted_id
# #     yield playlist
# #     if pls.already_exist(ret.inserted_id):
# #         pls.del_playlist(ret.inserted_id)


# def test_get_test_pname():
#     pid = upls._get_test_pname()
#     assert isinstance(pid, str)
#     assert 'playlist' in pid


# def test_get_test_uid():
#     uid = upls._get_test_uid()
#     assert isinstance(uid, str)


# # ---------- ADD FUNCTION TESTS -----------
# def test_add_playlist():
#     uid = upls._get_test_uid()
#     pname = upls._get_test_pname()
#     ret = upls.add_playlist(uid, pname)
#     assert ret.acknowledged
#     _id = ret.inserted_id
#     print(f'_id {type(_id)}: {_id}')
#     pid = upls._get_test_pid(str(_id))
#     print(f'uid {type(uid)}: {uid}')
#     print(f'pid {type(pid)}: {pid}')
#     assert upls.already_exist(uid, pid)
#     assert isinstance(ret, bool)
#     upls.del_playlist(uid, pid)
