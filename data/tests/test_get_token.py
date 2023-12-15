import data.get_Spotify_token as tkn


def test_get_token():
   token = tkn.get_token()
   assert isinstance(token, str)
   assert len(token) > 0
    