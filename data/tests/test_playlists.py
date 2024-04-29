import pytest

import data.playlists as pls
import data.songs as songs


# Yield a temporary playlist for testing
@pytest.fixture(scope='function')
def temp_playlist():
    playlist = pls.get_test_playlist()
    ret = pls.add_playlist(playlist['user_id'], playlist['name'])
    yield playlist
    if pls.already_exist(playlist['user_id'], playlist['name']):
        pls.del_playlist(playlist['user_id'], playlist['name'])


# ---------- GET FUNCTION TESTS -----------
def test_get_test_name():
    name = pls._get_test_name()
    assert isinstance(name, str)
    assert len(name) > pls.MIN_NAME_LEN


def test_get_test_user_id():
    user_id = pls._get_test_user_id()
    assert isinstance(user_id, str)
    assert len(user_id) > 0


def test_get_date():
    date = pls.get_date()
    assert isinstance(date, str)
    assert len(date) == 10


def test_get_test_playlist():
    playlist = pls.get_test_playlist()
    assert isinstance(playlist, dict)
    assert pls.USER_ID in playlist
    assert pls.DATE in playlist
    assert pls.NAME in playlist
    assert pls.SONGS in playlist


def test_get_playlists(temp_playlist):
    playlists = pls.get_playlists(temp_playlist['user_id'])
    assert isinstance(playlists, dict)
    assert len(playlists) > 0
    for name in playlists:
        assert isinstance(name, str)
        assert isinstance(playlists[name], dict)


def test_get_all_playlists(temp_playlist):
    playlists = pls.get_all_playlists()
    assert isinstance(playlists, dict)
    assert len(playlists) >= 0
    for playlist in playlists:
        assert isinstance(playlist, str)
        assert isinstance(playlists[playlist], dict)


def test_get_playlist(temp_playlist):
    user_id = temp_playlist['user_id']
    name = temp_playlist['name']
    playlist = pls.get_playlist(user_id, name)
    assert isinstance(playlist, dict)


def test_already_exist(temp_playlist):
    user_id = temp_playlist['user_id']
    name = temp_playlist['name']
    assert pls.already_exist(user_id, name) is True
    pls.del_playlist(user_id, name)


def test_already_exist_not_there():
    new_user_id = pls._get_test_user_id()
    new_name = pls._get_test_name()
    assert pls.already_exist(new_user_id, new_name) is False


def test_song_exists_in_playlist(temp_playlist):
    user_id = temp_playlist['user_id']
    name = temp_playlist['name']
    song_id = songs._gen_id()
    assert pls.song_exists_in_playlist(user_id, name, song_id) is False
    pls.update_add_songs_in_playlist(user_id, name, song_id)
    assert pls.song_exists_in_playlist(user_id, name, song_id)


def test_song_exists_in_playlist_not_there(temp_playlist):
    user_id = temp_playlist['user_id']
    name = temp_playlist['name']
    song_id = songs._gen_id()
    assert pls.song_exists_in_playlist(user_id, name, song_id) is False


# ---------- ADD FUNCTION TESTS -----------
def test_add_playlist():
    new_name = pls._get_test_name()
    new_user_id = pls._get_test_user_id()
    ret = pls.add_playlist(new_user_id, new_name)
    assert pls.already_exist(new_user_id, new_name)
    assert isinstance(ret, bool)
    pls.del_playlist(new_user_id, new_name)


def test_add_playlist_dup_name(temp_playlist):
    with pytest.raises(ValueError):
        pls.add_playlist(temp_playlist['user_id'], temp_playlist['name'])


# Testing for adding a playlist with empty name
def test_add_playlist_lt_1_char():
    new_name = ''
    new_user_id = pls._get_test_user_id()
    with pytest.raises(ValueError):
        pls.add_playlist(new_user_id, new_name)


# ---------- DELETE FUNCTION TESTS -----------
def test_del_playlist(temp_playlist):
    user_id = temp_playlist['user_id']
    name = temp_playlist['name']
    pls.del_playlist(user_id, name)
    assert pls.already_exist(user_id, name) is False


def test_del_playlist_not_there():
    user_id = pls._get_test_user_id()
    name = pls._get_test_name()
    with pytest.raises(ValueError):
        pls.del_playlist(user_id, name)


# ---------- UPDATE FUNCTION TESTS -----------
def test_update_playlist_name(temp_playlist):
    new_playlist_name = "thisisnew"
    user_id = temp_playlist['user_id']
    name = temp_playlist['name']
    pls.update_playlist_name(user_id, name, new_playlist_name)
    updated_playlist = pls.get_playlist(user_id, new_playlist_name)
    assert updated_playlist is not None
    assert updated_playlist.get("name") == new_playlist_name
    pls.del_playlist(user_id, new_playlist_name)


def test_update_playlist_name_dup_name(temp_playlist):
    user_id = temp_playlist['user_id']
    name = temp_playlist['name']
    with pytest.raises(ValueError):
        pls.update_playlist_name(user_id, name, name)


def test_update_playlist_name_lt_1_char(temp_playlist):
    new_name = ''
    with pytest.raises(ValueError):
        pls.update_playlist_name(temp_playlist['user_id'],
                                 temp_playlist['name'], new_name)


def test_update_add_songs_in_playlist(temp_playlist):
    user_id = temp_playlist['user_id']
    name = temp_playlist['name']
    new_song_id = songs._gen_id()
    assert isinstance(new_song_id, str)
    assert new_song_id not in temp_playlist[pls.SONGS]
    pls.update_add_songs_in_playlist(user_id, name, new_song_id)
    new_playlist = pls.get_playlist(user_id, name)
    assert new_song_id in new_playlist[pls.SONGS]


def test_update_add_songs_in_playlist_dup_song(temp_playlist):
    user_id = temp_playlist['user_id']
    name = temp_playlist['name']
    new_song_id = songs._gen_id()
    assert new_song_id not in temp_playlist[pls.SONGS]
    pls.update_add_songs_in_playlist(user_id, name, new_song_id)
    new_playlist = pls.get_playlist(user_id, name)
    assert new_song_id in new_playlist[pls.SONGS]
    with pytest.raises(ValueError):
        pls.update_add_songs_in_playlist(user_id, name, new_song_id)

# import pytest

# import data.playlists as pls


# # Yield a temporary playlist for testing
# @pytest.fixture(scope='function')
# def temp_playlist():
#     playlist = pls.get_test_playlist()
#     ret = pls.add_playlist(playlist['name'])
#     # playlist[pls.MONGO_ID] = pls.ObjectId(ret)
#     yield pls.get_playlist(ret)
#     if pls.already_exist(ret):
#         pls.del_playlist(ret)


# # ---------- GET FUNCTION TESTS -----------
# def test_get_test_name():
#     name = pls._get_test_name()
#     assert isinstance(name, str)
#     assert len(name) > pls.MIN_NAME_LEN


# def test_gen_id():
#     _id = pls._gen_id()
#     assert isinstance(_id, str)
#     assert len(_id) == pls.ID_LEN


# # def test_get_test_email():
# #     email = pls._get_test_email()
# #     assert isinstance(email, str)
# #     assert len(email) > 0
# #     # checking for email address validity
# #     assert '@' in email
# #     email_components = email.split('@')
# #     assert len(email_components[0]) >= 1
# #     assert '.' in email_components[1]


# def test_get_test_playlist():
#     playlist = pls.get_test_playlist()
#     assert isinstance(playlist, dict)
#     # assert pls.MONGO_ID in playlist
#     assert pls.NAME in playlist
#     assert pls.DATE in playlist


# # def test_get_playlists(temp_playlist):
# #     playlists = pls.get_playlists(temp_playlist['email'])
# #     assert isinstance(playlists, list)
# #     assert len(playlists) > 0
# #     for name in playlists:
# #         assert isinstance(name, str)
# #         assert len(name) >= pls.MIN_NAME_LEN


# def test_already_exist(temp_playlist):
#     _id = temp_playlist['_id']
#     assert pls.already_exist(_id) is True
#     pls.del_playlist(_id)


# def test_already_exist_not_there():
#     new_id = pls._gen_id()
#     assert pls.already_exist(new_id) is False


# def test_get_playlist(temp_playlist):
#     _id = temp_playlist['_id']
#     playlist = pls.get_playlist(_id)
#     assert isinstance(playlist, dict)
#     assert pls.MONGO_ID in playlist
#     assert pls.NAME in playlist
#     assert pls.DATE in playlist


# def test_get_playlist_not_there():
#     _id = pls._gen_id()
#     playlist = pls.get_playlist(_id)
#     assert playlist is None


# # def test_song_exists_in_playlist(temp_playlist):
# #     email = temp_playlist['email']
# #     name = temp_playlist['name']
# #     song_id = songs._gen_id()
# #     assert pls.song_exists_in_playlist(email, name, song_id) is False
# #     pls.update_add_songs_in_playlist(email, name, song_id)
# #     assert pls.song_exists_in_playlist(email, name, song_id)


# # def test_song_exists_in_playlist_not_there(temp_playlist):
# #     email = temp_playlist['email']
# #     name = temp_playlist['name']
# #     song_id = songs._gen_id()
# #     assert pls.song_exists_in_playlist(email, name, song_id) is False


# # ---------- ADD FUNCTION TESTS -----------
# def test_add_playlist():
#     new_name = pls._get_test_name()
#     ret = pls.add_playlist(new_name)
#     assert pls.already_exist(ret)
#     pls.del_playlist(ret)


# # def test_add_playlist_dup_name(temp_playlist):
# #     with pytest.raises(ValueError):
# #         pls.add_playlist(temp_playlist['email'], temp_playlist['name'])


# # Testing for adding a playlist with empty name
# def test_add_playlist_lt_1_char():
#     new_name = ''
#     with pytest.raises(ValueError):
#         pls.add_playlist(new_name)


# # # Testing for adding a playlist with invalid email containing no '@'
# # def test_add_playlist_invalid_email_v1():
# #     new_name = pls._get_test_name()
# #     new_email = 'randomstring'
# #     with pytest.raises(ValueError):
# #         pls.add_playlist(new_email, new_name)


# # # Testing for adding a playlist with email containing invalid domain
# # def test_add_playlist_invalid_email_v2():
# #     new_name = pls._get_test_name()
# #     new_email = 'random@string'
# #     with pytest.raises(ValueError):
# #         pls.add_playlist(new_email, new_name)


# # # Testing for adding a playlist with email containing invalid prefix
# # def test_add_playlist_invalid_email_v3():
# #     new_name = pls._get_test_name()
# #     new_email = '@randomstring.com'
# #     with pytest.raises(ValueError):
# #         pls.add_playlist(new_email, new_name)


# # ---------- DELETE FUNCTION TESTS -----------
# def test_del_playlist(temp_playlist):
#     _id = temp_playlist['_id']
#     assert pls.already_exist(_id)
#     pls.del_playlist(_id)
#     assert pls.already_exist(_id) is False


# def test_del_playlist_not_there():
#     _id = pls._gen_id()
#     with pytest.raises(ValueError):
#         pls.del_playlist(_id)


# # # ---------- UPDATE FUNCTION TESTS -----------
# # def test_update_playlist_name(temp_playlist):
# #     new_playlist_name = "thisisnew"
# #     email = temp_playlist['email']
# #     name = temp_playlist['name']
# #     pls.update_playlist_name(email, name, new_playlist_name)
# #     updated_playlist = pls.get_playlist(email, new_playlist_name)
# #     assert updated_playlist is not None
# #     assert updated_playlist.get("name") == new_playlist_name


# # def test_update_playlist_name_dup_name(temp_playlist):
# #     email = temp_playlist['email']
# #     name = temp_playlist['name']
# #     with pytest.raises(ValueError):
# #         pls.update_playlist_name(email, name, name)


# # def test_update_playlist_name_lt_1_char(temp_playlist):
# #     new_name = ''
# #     with pytest.raises(ValueError):
# #         pls.update_playlist_name(temp_playlist['email'],
# #                                  temp_playlist['name'], new_name)


# # def test_update_add_songs_in_playlist(temp_playlist):
# #     email = temp_playlist['email']
# #     name = temp_playlist['name']
# #     new_song_id = songs._gen_id()
# #     assert isinstance(new_song_id, str)
# #     assert new_song_id not in temp_playlist[pls.SONGS]
# #     pls.update_add_songs_in_playlist(email, name, new_song_id)
# #     new_playlist = pls.get_playlist(email, name)
# #     assert new_song_id in new_playlist[pls.SONGS]


# # def test_update_add_songs_in_playlist_dup_song(temp_playlist):
# #     email = temp_playlist['email']
# #     name = temp_playlist['name']
# #     new_song_id = songs._gen_id()
# #     assert new_song_id not in temp_playlist[pls.SONGS]
# #     pls.update_add_songs_in_playlist(email, name, new_song_id)
# #     new_playlist = pls.get_playlist(email, name)
# #     assert new_song_id in new_playlist[pls.SONGS]
# #     with pytest.raises(ValueError):
# #         pls.update_add_songs_in_playlist(email, name, new_song_id)
