import data.get_Spotify_playlists as playlists


# Test that the function returns a non-empty list of featured playlists
def test_get_featured_playlist():
   featured_playlists = playlists.get_featured_playlists()
   assert isinstance(featured_playlists, list)
   assert len(featured_playlists) > 0
