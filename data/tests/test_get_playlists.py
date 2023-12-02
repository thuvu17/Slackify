import pytest

import data.get_Spotify_playlists as playlists


# @pytest.fixture(scope='function')
def test_get_featured_playlist():
    featured_playlists = playlists.get_featured_playlists()
    assert isinstance(featured_playlists, list)
    assert len(featured_playlists) > 0
