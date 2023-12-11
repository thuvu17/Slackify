import pytest

import data.db_connect as dbc

TEST_DB = dbc.SLACKIFY_DB
TEST_COLLECT = 'songs'
# can be used for field and value:
NAME = 'name'
ARTIST = 'artist'
TEST_NAME = 'name'
TEST_ARTIST = 'Hello'
UPDATE = 'Update'
ALBUM = 'album'
GENRE = 'genre'
BPM = 'bpm'

TEST_INSERT = {
    NAME: TEST_NAME,
    ARTIST: TEST_ARTIST,
    ALBUM: 'unknown',
    GENRE: 'unknown',
    BPM: 0,
    }

# specifically for playlist tests
TEST_COLLECT_PL = 'playlists'
EMAIL = 'email'
TEST_EMAIL = 'random@email.com'
SONGS = 'songs'
SONGS_ID = 'randomSongID'
TEST_INSERT_PL = {
    NAME: TEST_NAME,
    EMAIL: TEST_EMAIL,
    SONGS: [SONGS_ID],
    }


@pytest.fixture(scope='function')
def temp_rec():
    dbc.connect_db()
    dbc.client[TEST_DB][TEST_COLLECT].insert_one(TEST_INSERT)
    # yield to our test function
    yield
    dbc.client[TEST_DB][TEST_COLLECT].delete_one({NAME: TEST_NAME,
                                                  ARTIST: TEST_ARTIST})


@pytest.fixture(scope='function')
def temp_rec_playlist():
    dbc.connect_db()
    dbc.client[TEST_DB][TEST_COLLECT_PL].insert_one(TEST_INSERT_PL)
    # yield to our test function
    yield
    dbc.client[TEST_DB][TEST_COLLECT_PL].delete_one({NAME: TEST_NAME,
                                                  EMAIL: TEST_EMAIL})


def test_fetch_one(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {NAME: TEST_NAME, ARTIST: TEST_ARTIST})
    assert ret is not None


def test_fetch_one_not_there(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {NAME: 'not a field value in db!'})
    assert ret is None


def test_fetch_all_as_list(temp_rec_playlist):
    ret = dbc.fetch_all_as_list(TEST_COLLECT_PL, {EMAIL: TEST_EMAIL}, NAME)
    assert ret is not None


def test_update_doc(temp_rec):
    dbc.update_doc(TEST_COLLECT, {TEST_NAME: TEST_NAME}, {TEST_NAME: UPDATE})
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_NAME: UPDATE})
    assert ret is not None
