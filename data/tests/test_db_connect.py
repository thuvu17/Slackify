import pytest

import data.db_connect as dbc

TEST_DB = dbc.SLACKIFY_DB
TEST_COLLECT = 'songs'
# can be used for field and value:
TEST_FIELD = 'name'
TEST_VALUE = 'Hello'
TEST_INSERT = {
    "name":"Hello",
    "artist":"Adele",
    "bpm": 98
    }


@pytest.fixture(scope='function')
def temp_rec():
    dbc.connect_db()
    dbc.client[TEST_DB][TEST_COLLECT].insert_one(TEST_INSERT)
    # yield to our test function
    yield
    dbc.client[TEST_DB][TEST_COLLECT].delete_one({TEST_FIELD: TEST_VALUE})


def test_fetch_one(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_FIELD: TEST_VALUE})
    assert ret is not None


def test_fetch_one_not_there(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_FIELD: 'not a field value in db!'})
    assert ret is None
