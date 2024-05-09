import pytest

import data.db_connect as dbc

TEST_DB = dbc.SLACKIFY_DB
TEST_COLLECT = 'songs'
# can be used for field and value:
NAME = 'name'
ARTIST = 'artist'
TEST_NAME = 'name'
TEST_ARTIST = 'Hello'
TEST_LIST = 'test_list'
DATE_CREATED = 'date_created'
UPDATE = 'Update'
APPEND = 'Append'
ALBUM = 'album'
ENERGY = 'energy'
BPM = 'bpm'
TEST_INSERT = {
    NAME: TEST_NAME,
    ARTIST: TEST_ARTIST,
    ALBUM: 'unknown',
    ENERGY: 'unknown',
    BPM: 0,
    }

# specifically for playlist tests
TEST_COLLECT_PL = 'playlists'
EMAIL = 'email'
TEST_EMAIL = 'random@email.com'
TEST_DATE = "2024-05-06"
SONGS = 'songs'
SONGS_ID = 'randomSongID'
TEST_INSERT_PL = {
    NAME: TEST_NAME,
    DATE_CREATED: TEST_DATE,
    EMAIL: TEST_EMAIL,
    SONGS: [SONGS_ID],
    }

# specifically for user tests
TEST_COLLECT_USR = 'users'
PASSWORD = 'password'
TEST_PASSWORD = 'iloveslackify'
TEST_INSERT_USR = {
    NAME: TEST_NAME,
    EMAIL: TEST_EMAIL,
    PASSWORD: TEST_PASSWORD,
    TEST_LIST: [],
    }


# temporary object inserted in the song collection for testing
@pytest.fixture(scope='function')
def temp_rec():
    dbc.connect_db()
    dbc.client[TEST_DB][TEST_COLLECT].insert_one(TEST_INSERT)
    # yield to our test function
    yield
    dbc.client[TEST_DB][TEST_COLLECT].delete_one({NAME: TEST_NAME,
                                                  ARTIST: TEST_ARTIST})


# temporary object inserted in the playlist collection for testing
@pytest.fixture(scope='function')
def temp_rec_playlist():
    dbc.connect_db()
    dbc.client[TEST_DB][TEST_COLLECT_PL].insert_one(TEST_INSERT_PL)
    # yield to our test function
    yield
    dbc.client[TEST_DB][TEST_COLLECT_PL].delete_one({EMAIL: TEST_EMAIL,
                                                     NAME: TEST_NAME})


# temporary object inserted in the user collection for testing
@pytest.fixture(scope='function')
def temp_rec_user():
    dbc.connect_db()
    dbc.client[TEST_DB][TEST_COLLECT_USR].insert_one(TEST_INSERT_USR)
    # yield to our test function
    yield
    dbc.client[TEST_DB][TEST_COLLECT_USR].delete_one({EMAIL: TEST_EMAIL})


# ---------- FETCH FUNCTION TESTS -----------
def test_fetch_one(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {NAME: TEST_NAME,
                                       ARTIST: TEST_ARTIST})
    assert ret is not None


def test_fetch_one_not_there(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {NAME: 'not a field value in db!'})
    assert ret is None


def test_fetch_all_songs_as_dict(temp_rec):
    ret = dbc.fetch_all_songs_as_dict(TEST_COLLECT)
    assert ret is not None
    assert isinstance(ret, dict)
    assert len(ret) > 0


def test_fetch_all_as_dict(temp_rec_user):
    ret = dbc.fetch_all_as_dict(EMAIL, TEST_COLLECT_USR)
    assert ret is not None
    assert isinstance(ret, dict)
    assert len(ret) > 0


def test_fetch_all_as_list(temp_rec_playlist):
    ret = dbc.fetch_all_as_list(TEST_COLLECT_PL, {EMAIL: TEST_EMAIL}, NAME)
    assert isinstance(ret, list)
    assert ret is not None
    assert len(ret) > 0


def test_fetch_all_as_dict_with_filter(temp_rec_playlist):
    ret = dbc.fetch_all_as_dict_with_filter(TEST_COLLECT_PL,
                                            {EMAIL: TEST_EMAIL,
                                             NAME: TEST_NAME})
    assert isinstance(ret, dict)
    assert ret is not None
    assert len(ret) > 0


# ---------- UPDATE FUNCTION TEST -----------
def test_update_doc(temp_rec):
    # check if doc successfully added
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: TEST_NAME})
    assert ret is not None
    dbc.update_doc(TEST_COLLECT, {TEST_NAME: TEST_NAME}, {TEST_NAME: UPDATE})
    # check if doc successfully updated
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: UPDATE})
    assert ret is not None
    dbc.del_one(TEST_COLLECT, {TEST_NAME: UPDATE})
    # check if doc successfully deleted
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: UPDATE})
    assert ret is None


def test_append_doc(temp_rec):
    # check if doc successfully added
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: TEST_NAME})
    assert ret is not None
    dbc.append_doc(TEST_COLLECT, {TEST_NAME: TEST_NAME}, {TEST_LIST: APPEND})
    # check if doc successfully updated
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_LIST: APPEND})
    assert ret is not None
    dbc.del_one(TEST_COLLECT, {TEST_LIST: APPEND})
    # check if doc successfully deleted
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_LIST: APPEND})
    assert ret is None
