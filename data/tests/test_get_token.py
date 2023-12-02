import pytest

import data.get_Spotify_token as tkn


# @pytest.fixture(scope='function')
def test_get_token():
    token = tkn.get_token()
    assert isinstance(token, str)
    assert len(token) > 0
    