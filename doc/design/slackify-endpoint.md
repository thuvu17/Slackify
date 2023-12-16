# Slackify Endpoint

## OVERVIEW

This is a Flask application with various endpoints for managing users, songs, and playlists. Here's a brief overview of the endpoints:

### HelloWorld EP
>A simple test endpoint to check if the server is running.
- URL: /hello
- Input: None
- Output: JSON response with the message "hello world."
- Method: GET

### Endpoints EP
>Returns a list of all available endpoints in the server.
- URL: /endpoints
- Input: None
- Output: JSON response containing a list of available endpoints.
- Method: GET

## MENU ENDPOINTS
Down here is all the endpoints that load menus
### MainMenu EP:
>Returns the main menu with options to sign in, sign up, display most popular songs, etc. (more to come)
- URL: /MainMenu
- Input: None
- Output: JSON response representing the main menu.
- Method: GET

### UserMenu EP:
>Returns the user menu for the user with given email.
>This endpoints will be called by a successful sign in
- URL: /user_menu/&lt;email&gt;
- Input: 
  - Path parameter: **email** (User email)
- Output: JSON response representing the user menu.
- Method: GET

## USER ENDPOINTS
Down below are all endpoints related to users: GET, POST, DEL
### GetUser EP:
>Returns a list of all users
- URL: /users
- Input: None
- Output: JSON response containing a list of current users.
- Methods: GET

### AddUser EP:
>Adds a new user
- URL: /users
- Input: 
  - JSON payload containing user data (name, email, password).
  - Must be a valid email (e.g. prefix@domain.com)
  - Name must have more than 2 characters
  - Password must have more than 8 characters
```cpp
  user_fields = api.model('NewUser', {
    users.NAME: fields.String,
    users.EMAIL: fields.String,
    users.PASSWORD: fields.String,
}
```
- Output: JSON response indicating success or failure in adding a user.
- Methods: POST

### DelUser EP:
>Deletes a user by email.
- URL: /users/delete/&lt;email&gt;
- Input:
  - Path parameter: **email** (User email)
- Output: JSON response indicating success or failure in deleting a user.
- Method: DELETE

## SONG ENDPOINTS
Down below are all endpoints related to songs: GET, POST, DEL
### ListSong EP:
>Returns a list of all songs
- URL: /songs
- Input: None
- Output: JSON response containing a list of current songs.
- Methods: GET

### AddSong EP:
>Adds a new song.
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
- Output: JSON response indicating success or failure in adding a song.
- Methods: POST

 
### DelSong EP:
>Deletes a song by name and artist.
- URL: /songs/delete/&lt;name&gt;/&lt;artist&gt;
- Input:
  - Path parameters: **name** (Song name), **artist** (Song artist)
- Output: JSON response indicating success or failure in deleting a song.
- Method: DELETE

## PLAYLIST ENDPOINTS
Down below are all endpoints related to playlist: GET, POST, DEL. Email will be taken from the session.
### Playlists EP:
>Adds a new playlist.
- URL: /playlists
- Input:
  - JSON payload containing playlist data (email, name)
  - Playlist name cannot be an empty string
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

### GetPlaylists EP:
>Returns all playlists for a specified user.
- URL: /playlists/get/&lt;email&gt;
- Input:
  - Path parameter: email (User email)
- Output: JSON response containing a list of playlists for a specific user.
- Method: GET

### DelPlaylist EP:
>Deletes a playlist by user email and playlist name.
- URL: /playlists/delete/&lt;email&gt;/&lt;name&gt;
- Input:
  - Path parameters: **email** (User email), **name** (Playlist name)
- Output: JSON response indicating success or failure in deleting a playlist.
- Method: DELETE

## AUTHENTICATION ENDPOINTS
This takes care of signing in, signing up, and signing out
### SignIn EP:
>Authenticates a user and redirects to the user menu.
- URL: /sign_in/&lt;email&gt;/&lt;password&gt;
- Input:
  - Path parameters: **email** (User email), **password** (User password)
- Output: Redirects to the user menu if authentication is successful. Otherwise, returns an error.
- Method: GET

### SignUp EP:
>Adds a new user and redirects to the user menu.
- URL: /sign_up/&lt;email&gt;/&lt;password&gt;/&lt;username&gt;
- Input:
  - Path parameters: **email** (User email), **password** (User password), **username** (User name)
- Output: Redirects to the user menu if user registration is successful. Otherwise, returns an error.
- Method: GET

### SignOut EP:
>Logs out a user.
- URL: /sign_out/&lt;email&gt;
- Input:
  - Path parameter: **email** (User email)
- Output: JSON response indicating success or failure in signing out.
- Method: GET

# Spotify end-points in the backend
## OVERVIEW

These endpoints are sample data requested from Spotify to store in Slackify's database
(We haven't designed an implementation for this data and plan to do it next semester)

### Get Spotify Token
>Send a POST request to the token endpoint URI and return a string of the access token
- URL: https://accounts.spotify.com/api/token
- Input:
  - client_id
  - client_secret
- Method: POST

### Get Spotify Playlists
>Send a GET request to Spotify to get a list of featured playlists. Limit is set to 50
- URL: https://api.spotify.com/v1/browse/featured-playlists/?limit=50
- Input:
  - Access Token
- Method: GET

### Get Spotify popular songs
>Send a GET request to Spotify to get a list of the first ten tracks in Spotify's Most Played All-Time playlist

- URL: https://api.spotify.com/v1/playlists/2YRe7HRKNRvXdJBp9nXFza/tracks?offset=0&limit=10
- Input:
  - Access Token
- Method: GET
