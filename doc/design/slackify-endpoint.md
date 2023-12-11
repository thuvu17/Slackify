# Slackify Endpoint

## OVERVIEW

This is a Flask application with various endpoints for managing users, songs, and playlists. Here's a brief overview of the endpoints:

## HelloWorld Endpoint
- URL: /hello
- Input: None
- Method: GET
- Description: A simple test endpoint to check if the server is running.

## Endpoint endpoint
- URL: /endpoints
- Input: None
- Method: GET
- Description: Returns a list of all available endpoints in the system.

## MainMenu Endpoint:
- URL: /MainMenu
- Input: None
- Method: GET
- Description: Returns the main menu with choices related to songs.

## UserMenu Endpoint:
- URL: /user_menu/<email>
- Input: 
  - Path parameter: **email** (User email)
- Method: GET
- Description: Returns the user menu for a specific user.

## Users Endpoint:
- URL: /users
- Input: 
  - JSON payload containing user data (name, email, password).
- Methods: GET, POST
- Description:
  - GET: Returns a list of all users.
  - POST: Adds a new user.

## DelUser Endpoint:
- URL: /users/delete/<email>
- Input:
  - Path parameter: **email** (User email)
- Method: DELETE
- Description: Deletes a user by email.

## DelSong Endpoint:
- URL: /songs/delete/<name>/<artist>
- Input:
  - Path parameters: **name** (Song name), **artist** (Song artist)
- Method: DELETE
- Description: Deletes a song by name and artist.

## Songs Endpoint:
- URL: /songs
- Input:
  - JSON payload containing song data (name, artist, album, genre, bpm)
- Methods: GET, POST
- Description:
  - GET: Returns a list of all songs.
  - POST: Adds a new song.

## DelPlaylist Endpoint:
- URL: /playlists/delete/<email>/<name>
- Input:
  - Path parameters: **email** (User email), **name** (Playlist name)
- Method: DELETE
- Description: Deletes a playlist by user email and playlist name.

## Playlists Endpoint:
- URL: /playlists
- Input:
  - JSON payload containing playlist data (email, name)
- Method: POST
- Description: Adds a new playlist.

## GetPlaylists Endpoint:
- URL: /playlists/get/<email>
- Input:
  - Path parameter: email (User email)
- Method: GET
- Description: Returns all playlists for a specific user.

## SignIn Endpoint:
- URL: /sign_in/<email>/<password>
- Input:
  - Path parameters: **email** (User email), **password** (User password)
- Method: GET
- Description: Authenticates a user and redirects to the user menu.

## SignUp Endpoint:
- URL: /sign_up/<email>/<password>/<username>
- Input:
  - Path parameters: **email** (User email), **password** (User password), **username** (User name)
- Method: GET
- Description: Adds a new user and redirects to the user menu.

## SignOut Endpoint:
- URL: /sign_out/<email>
- Input:
  - Path parameter: **email** (User email)
- Method: GET
- Description: Logs out a user.
