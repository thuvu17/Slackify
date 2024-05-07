import data.get_Spotify_token as tkn


# Test that the get_token function returns a valid access token string
def test_get_token():
   token = tkn.get_token()
   assert isinstance(token, str)
   assert len(token) > 0
