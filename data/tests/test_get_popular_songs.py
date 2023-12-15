import data.get_most_popular_songs as songs


def test_get_featured_playlist():
   popular_songs = songs.get_most_popular_songs()
   assert isinstance(popular_songs, list)
   assert len(popular_songs) == 10
   