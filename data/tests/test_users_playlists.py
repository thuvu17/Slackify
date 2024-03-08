# import pytest
# from bson import ObjectId

# import data.users_playlists as upls

# # Yield a temporary user-playlist for testing
# @pytest.fixture(scope='function')
# def temp_schema():
#     schema = upls._get_test_schema()
#     uid = schema[upls.USER_ID]
#     pid = schema[upls.PLAYLIST_ID]
#     ret = upls.add_playlist(uid, pid)
#     yield schema
#     if upls.already_exist(uid, pid):
#         upls.del_playlist(uid, pid)


# def test_get_test_uid():
#     uid = upls._get_test_uid()
#     assert isinstance(uid, str)


# def test_get_test_pid():
#     pid = upls._get_test_pid()
#     assert isinstance(pid, str)


# def test_get_test_schema():
#     schema = upls._get_test_schema()
#     assert isinstance(schema, dict)
#     assert upls.USER_ID in schema
#     assert upls.PLAYLIST_ID in schema


# def test_get_playlist_ids_as_list(temp_schema):
#     uid = temp_schema['user_id']
#     playlist_ids = upls.get_playlist_ids_as_list(uid)
#     assert isinstance(playlist_ids, list)
#     assert len(playlist_ids) > 0


# def test_get_playlist_ids_as_list_not_there():
#     uid = upls._get_test_uid()
#     playlist_ids = upls.get_playlist_ids_as_list(uid)
#     assert isinstance(playlist_ids, list)
#     assert len(playlist_ids) == 0


# def test_already_exist(temp_schema):
#     uid = temp_schema['user_id']
#     pid = temp_schema['playlist_id']
#     assert upls.already_exist(uid, pid) is True
#     upls.del_playlist(uid, pid)


# def test_already_exist_not_there():
#     new_uid = upls._get_test_uid()
#     new_pid = upls._get_test_pid()
#     assert upls.already_exist(new_uid, new_pid) is False


# # ---------- ADD FUNCTION TESTS -----------
# def test_add_playlist():
#     uid = upls._get_test_uid()
#     pid = upls._get_test_pid()
#     ret = upls.add_playlist(uid, pid)
#     assert isinstance(ret, bool)
#     assert upls.already_exist(uid, pid)
#     upls.del_playlist(uid, pid)
#     assert upls.already_exist(uid, pid) is False


# # ---------- DELETE FUNCTION TESTS -----------
# def test_del_playlist(temp_schema):
#     uid = temp_schema['user_id']
#     pid = temp_schema['playlist_id']
#     assert upls.already_exist(uid, pid)
#     upls.del_playlist(uid, pid)
#     assert upls.already_exist(uid, pid) is False


# def test_del_playlist_not_there():
#     uid = upls._get_test_uid()
#     pid = upls._get_test_pid()
#     with pytest.raises(ValueError):
#         upls.del_playlist(uid, pid)
