# Slackify Endpoint

## OVERVIEW

This is a Flask application with various endpoints for managing users, songs, and playlists. Here's a brief overview of the endpoints:

## HelloWorld Endpoint
- URL: /hello
- Input: None
- Output: JSON response with the message "hello world."
- Method: GET
- Description: A simple test endpoint to check if the server is running.

## Endpoint endpoint
- URL: /endpoints
- Input: None
- Output: JSON response containing a list of available endpoints.
- Method: GET
- Description: Returns a list of all available endpoints in the system.

## MainMenu Endpoint:
- URL: /MainMenu
- Input: None
- Output: JSON response representing the main menu.
- Method: GET
- Description: Returns the main menu with choices related to songs.

## UserMenu Endpoint:
- URL: /user_menu/<email>
- Input: 
  - Path parameter: **email** (User email)
- Output: JSON response representing the user menu.
- Method: GET
- Description: Returns the user menu for a specific user.

## Users Endpoint:
- URL: /users
- Input: 
  - JSON payload containing user data (name, email, password).
- Output:
  1. JSON response containing a list of current users.
  2. JSON response indicating success or failure in adding a user.
- Methods: GET, POST
- Description:
  - GET: Returns a list of all users.
  - POST: Adds a new user.

## DelUser Endpoint:
- URL: /users/delete/<email>
- Input:
  - Path parameter: **email** (User email)
- Output: JSON response indicating success or failure in deleting a user.
- Method: DELETE
- Description: Deletes a user by email.

## DelSong Endpoint:
- URL: /songs/delete/<name>/<artist>
- Input:
  - Path parameters: **name** (Song name), **artist** (Song artist)
- Output: JSON response indicating success or failure in deleting a song.
- Method: DELETE
- Description: Deletes a song by name and artist.

## Songs Endpoint:
- URL: /songs
- Input:
  - JSON payload containing song data (name, artist, album, genre, bpm)
- Output:
  1. JSON response containing a list of current songs.
  2. JSON response indicating success or failure in adding a song.
- Methods: GET, POST
- Description:
  - GET: Returns a list of all songs.
  - POST: Adds a new song.

## DelPlaylist Endpoint:
- URL: /playlists/delete/<email>/<name>
- Input:
  - Path parameters: **email** (User email), **name** (Playlist name)
- Output: JSON response indicating success or failure in deleting a playlist.
- Method: DELETE
- Description: Deletes a playlist by user email and playlist name.

## Playlists Endpoint:
- URL: /playlists
- Input:
  - JSON payload containing playlist data (email, name)
- Output:
  1. JSON response indicating success or failure in adding a playlist.
  2. JSON response containing a list of current playlists.
- Method: POST
- Description: Adds a new playlist.

## GetPlaylists Endpoint:
- URL: /playlists/get/<email>
- Input:
  - Path parameter: email (User email)
- Output: JSON response containing a list of playlists for a specific user.
- Method: GET
- Description: Returns all playlists for a specific user.

## SignIn Endpoint:
- URL: /sign_in/<email>/<password>
- Input:
  - Path parameters: **email** (User email), **password** (User password)
- Output: Redirects to the user menu if authentication is successful. Otherwise, returns an error.
- Method: GET
- Description: Authenticates a user and redirects to the user menu.

## SignUp Endpoint:
- URL: /sign_up/<email>/<password>/<username>
- Input:
  - Path parameters: **email** (User email), **password** (User password), **username** (User name)
- Output: Redirects to the user menu if user registration is successful. Otherwise, returns an error.
- Method: GET
- Description: Adds a new user and redirects to the user menu.

## SignOut Endpoint:
- URL: /sign_out/<email>
- Input:
  - Path parameter: **email** (User email)
- Output: JSON response indicating success or failure in signing out.
- Method: GET
- Description: Logs out a user.

### Spotify end-points in the backend
## Overview
- These endpoints are sample data requested from Spotify to store in Slackify's database
- We haven't designed an implementation for this data and plan to do it next semester

## Get Spotify Token
- URL: https://accounts.spotify.com/api/token
- Input:
  - client_id
  - client_secret
- Method: POST
- Description: Send a POST request to the token endpoint URI and return a string of the access token

## Get Spotify Playlists
- URL: https://api.spotify.com/v1/browse/featured-playlists/?limit=50
- Input:
  - Access Token
- Method: GET
- Description: Send a GET request to Spotify to get a list of featured playlists. Limit is set to 50

## Get Spotify popular songs
- URL: https://api.spotify.com/v1/playlists/2YRe7HRKNRvXdJBp9nXFza/tracks?offset=0&limit=10
- Input:
  - Access Token
- Method: GET
- Description: Send a GET request to Spotify to get a list of the first ten tracks in Spotify's Most Played All-Time playlist