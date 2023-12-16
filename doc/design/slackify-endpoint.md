# Slackify Endpoint

## OVERVIEW

This is a Flask application with various endpoints for managing users, songs, and playlists. Here's a brief overview of the endpoints:

### HelloWorld EP
- URL: /hello
- Input: None
- Output: JSON response with the message "hello world."
- Method: GET
- Description: A simple test endpoint to check if the server is running.

### Endpoints EP
- URL: /endpoints
- Input: None
- Output: JSON response containing a list of available endpoints.
- Method: GET
- Description: Returns a list of all available endpoints in the server.

## MENU ENDPOINTS
### MainMenu EP:
- URL: /MainMenu
- Input: None
- Output: JSON response representing the main menu.
- Method: GET
- Description: Returns the main menu with options to sign in, sign up, display most popular songs, etc. (more to come)

### UserMenu EP:
- URL: /user_menu/&lt;email&gt;
- Input: 
  - Path parameter: **email** (User email)
- Output: JSON response representing the user menu.
- Method: GET
- Description: Returns the user menu for the user with given email.

## USER ENDPOINTS
### Users EP:
- URL: /users
- Input: 
  - JSON payload containing user data (name, email, password).
```cpp
  user_fields = api.model('NewUser', {
    users.NAME: fields.String,
    users.EMAIL: fields.String,
    users.PASSWORD: fields.String,
}
```
- Output:
  1. JSON response containing a list of current users.
  2. JSON response indicating success or failure in adding a user.
- Methods: GET, POST
- Description:
  - GET: Returns a list of all users.
  - POST: Adds a new user.

### DelUser EP:
- URL: /users/delete/&lt;email&gt;
- Input:
  - Path parameter: **email** (User email)
- Output: JSON response indicating success or failure in deleting a user.
- Method: DELETE
- Description: Deletes a user by email.

## SONG ENDPOINTS
### Songs EP:
- URL: /songs
- Input:
  - JSON payload containing song data (name, artist, album, genre, bpm)
```cpp
song_fields = api.model('NewSong', {
    songs.NAME: fields.String,
    songs.ARTIST: fields.String,
    songs.ALBUM: fields.String,
    songs.GENRE: fields.String,
    songs.BPM: fields.Integer,
}
```
- Output:
  1. JSON response containing a list of current songs.
  2. JSON response indicating success or failure in adding a song.
- Methods: GET, POST
- Description:
  - GET: Returns a list of all songs.
  - POST: Adds a new song.
 
### DelSong EP:
- URL: /songs/delete/&lt;name&gt;/&lt;artist&gt;
- Input:
  - Path parameters: **name** (Song name), **artist** (Song artist)
- Output: JSON response indicating success or failure in deleting a song.
- Method: DELETE
- Description: Deletes a song by name and artist.

## PLAYLIST ENDPOINTS
### Playlists EP:
- URL: /playlists
- Input:
  - JSON payload containing playlist data (email, name)
```cpp
playlist_fields = api.model('NewPlaylist', {
    plists.EMAIL: fields.String,
    plists.NAME: fields.String,
    plists.SONGS: fields.List(fields.String),
}
```
- Output:
  1. JSON response indicating success or failure in adding a playlist.
  2. JSON response containing a list of current playlists.
- Method: POST
- Description: Adds a new playlist.

### GetPlaylists EP:
- URL: /playlists/get/&lt;email&gt;
- Input:
  - Path parameter: email (User email)
- Output: JSON response containing a list of playlists for a specific user.
- Method: GET
- Description: Returns all playlists for a specific user.

### DelPlaylist EP:
- URL: /playlists/delete/&lt;email&gt;/&lt;name&gt;
- Input:
  - Path parameters: **email** (User email), **name** (Playlist name)
- Output: JSON response indicating success or failure in deleting a playlist.
- Method: DELETE
- Description: Deletes a playlist by user email and playlist name.

## AUTHENTICATION ENDPOINTS
### SignIn EP:
- URL: /sign_in/&lt;email&gt;/&lt;password&gt;
- Input:
  - Path parameters: **email** (User email), **password** (User password)
- Output: Redirects to the user menu if authentication is successful. Otherwise, returns an error.
- Method: GET
- Description: Authenticates a user and redirects to the user menu.

### SignUp EP:
- URL: /sign_up/&lt;email&gt;/&lt;password&gt;/&lt;username&gt;
- Input:
  - Path parameters: **email** (User email), **password** (User password), **username** (User name)
- Output: Redirects to the user menu if user registration is successful. Otherwise, returns an error.
- Method: GET
- Description: Adds a new user and redirects to the user menu.

### SignOut EP:
- URL: /sign_out/&lt;email&gt;
- Input:
  - Path parameter: **email** (User email)
- Output: JSON response indicating success or failure in signing out.
- Method: GET
- Description: Logs out a user.

# Spotify end-points in the backend
## OVERVIEW

These endpoints are sample data requested from Spotify to store in Slackify's database
(We haven't designed an implementation for this data and plan to do it next semester)

### Get Spotify Token
- URL: https://accounts.spotify.com/api/token
- Input:
  - client_id
  - client_secret
- Method: POST
- Description: Send a POST request to the token endpoint URI and return a string of the access token

### Get Spotify Playlists
- URL: https://api.spotify.com/v1/browse/featured-playlists/?limit=50
- Input:
  - Access Token
- Method: GET
- Description: Send a GET request to Spotify to get a list of featured playlists. Limit is set to 50

### Get Spotify popular songs
- URL: https://api.spotify.com/v1/playlists/2YRe7HRKNRvXdJBp9nXFza/tracks?offset=0&limit=10
- Input:
  - Access Token
- Method: GET
- Description: Send a GET request to Spotify to get a list of the first ten tracks in Spotify's Most Played All-Time playlist
