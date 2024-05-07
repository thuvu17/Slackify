import data.get_most_popular_songs as songs


# Test that the function returns a list of 10 songs,
# confirming successful retrieval of popular songs
def test_get_featured_playlist():
   popular_songs = songs.get_most_popular_songs()
   assert isinstance(popular_songs, list)
   assert len(popular_songs) == 10
