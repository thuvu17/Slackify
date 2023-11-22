import pytest

import data.db_connect as dbc

TEST_DB = dbc.SLACKIFY_DB
TEST_COLLECT = 'songs'
# can be used for field and value:
NAME = 'name'
ARTIST = 'artist'
TEST_NAME = 'name'
TEST_ARTIST = 'Hello'
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


@pytest.fixture(scope='function')
def temp_rec():
    dbc.connect_db()
    dbc.client[TEST_DB][TEST_COLLECT].insert_one(TEST_INSERT)
    # yield to our test function
    yield
    dbc.client[TEST_DB][TEST_COLLECT].delete_one({NAME: TEST_NAME,
                                                  ARTIST: TEST_ARTIST})


def test_fetch_one(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {NAME: TEST_NAME, ARTIST: TEST_ARTIST})
    assert ret is not None


def test_fetch_one_not_there(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {NAME: 'not a field value in db!'})
    assert ret is None
