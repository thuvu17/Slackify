import pytest

import data.playlists as pls


# Yield a temporary playlist for testing
@pytest.fixture(scope='function')
def temp_playlist():
    playlist = pls.get_test_playlist()
    ret = pls.add_playlist(playlist['email'], playlist['name'])
    yield playlist
    if pls.already_exist(playlist['email'], playlist['name']):
        pls.del_playlist(playlist['email'], playlist['name'])


# ---------- GET FUNCTION TESTS -----------
def test_get_test_name():
    name = pls._get_test_name()
    assert isinstance(name, str)
    assert len(name) > pls.MIN_NAME_LEN


def test_get_test_email():
    email = pls._get_test_email()
    assert isinstance(email, str)
    assert len(email) > 0
    # checking for email address validity
    assert '@' in email
    email_components = email.split('@')
    assert len(email_components[0]) >= 1
    assert '.' in email_components[1]


def test_get_test_playlist():
    playlist = pls.get_test_playlist()
    assert isinstance(playlist, dict)
    assert pls.EMAIL in playlist
    assert pls.NAME in playlist
    assert pls.SONGS in playlist


def test_get_playlists(temp_playlist):
    playlists = pls.get_playlists(temp_playlist['email'])
    assert isinstance(playlists, list)
    assert len(playlists) > 0
    for name in playlists:
        assert isinstance(name, str)
        assert len(name) >= pls.MIN_NAME_LEN


# ---------- ADD FUNCTION TESTS -----------
def test_add_playlist():
    new_name = pls._get_test_name()
    new_email = pls._get_test_email()
    ret = pls.add_playlist(new_email, new_name)
    assert pls.already_exist(new_email, new_name)
    assert isinstance(ret, bool)
    pls.del_playlist(new_email, new_name)


def test_add_playlist_dup_name(temp_playlist):
    with pytest.raises(ValueError):
        pls.add_playlist(temp_playlist['email'], temp_playlist['name'])


# Testing for adding a playlist with empty name
def test_add_playlist_lt_1_char():
    new_name = ''
    new_email = pls._get_test_email()
    with pytest.raises(ValueError):
        pls.add_playlist(new_email, new_name)


# Testing for adding a playlist with invalid email containing no '@'
def test_add_playlist_invalid_email_v1():
    new_name = pls._get_test_name()
    new_email = 'randomstring'
    with pytest.raises(ValueError):
        pls.add_playlist(new_email, new_name)


# Testing for adding a playlist with email containing invalid domain
def test_add_playlist_invalid_email_v2():
    new_name = pls._get_test_name()
    new_email = 'random@string'
    with pytest.raises(ValueError):
        pls.add_playlist(new_email, new_name)


# Testing for adding a playlist with email containing invalid prefix
def test_add_playlist_invalid_email_v3():
    new_name = pls._get_test_name()
    new_email = '@randomstring.com'
    with pytest.raises(ValueError):
        pls.add_playlist(new_email, new_name)


# ---------- DELETE FUNCTION TESTS -----------
def test_del_playlist(temp_playlist):
    email = temp_playlist['email']
    name = temp_playlist['name']
    pls.del_playlist(email, name)
    assert pls.already_exist(email, name) is False


def test_del_playlist_not_there():
    email = pls._get_test_email()
    name = pls._get_test_name()
    with pytest.raises(ValueError):
        pls.del_playlist(email, name)
