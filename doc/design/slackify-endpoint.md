# Slackify Endpoint

** OVERVIEW
This is a Flask application with various endpoints for managing users, songs, and playlists. Here's a brief overview of the endpoints:
** HelloWorld Endpoint
- URL: /hello
- Method: GET
- Description: A simple test endpoint to check if the server is running.

** Endpoint endpoint
- URL: /endpoints
- Method: GET
- Description: Returns a list of all available endpoints in the system.

** MainMenu Endpoint:
- URL: /MainMenu
- Method: GET
- Description: Returns the main menu with choices related to songs.

** UserMenu Endpoint:
- URL: /user_menu/<email>
- Method: GET
- Description: Returns the user menu for a specific user.

** Users Endpoint:
- URL: /users
- Methods: GET, POST
- Description:
  - GET: Returns a list of all users.
  - POST: Adds a new user.

** DelUser Endpoint:
- URL: /users/delete/<email>
- Method: DELETE
- Description: Deletes a user by email.

** DelSong Endpoint:
- URL: /songs/delete/<name>/<artist>
- Method: DELETE
- Description: Deletes a song by name and artist.

** Songs Endpoint:
- URL: /songs
= Methods: GET, POST
- Description:
  - GET: Returns a list of all songs.
  - POST: Adds a new song.

** DelPlaylist Endpoint:
- URL: /playlists/delete/<email>/<name>
- Method: DELETE
- Description: Deletes a playlist by user email and playlist name.

** Playlists Endpoint:
- URL: /playlists
- Method: POST
- Description: Adds a new playlist.

** GetPlaylists Endpoint:
- URL: /playlists/get/<email>
- Method: GET
- Description: Returns all playlists for a specific user.

** SignIn Endpoint:
- URL: /sign_in/<email>/<password>
- Method: GET
- Description: Authenticates a user and redirects to the user menu.

** SignUp Endpoint:
- URL: /sign_up/<email>/<password>/<username>
- Method: GET
- Description: Adds a new user and redirects to the user menu.

** SignOut Endpoint:
- URL: /sign_out/<email>
- Method: GET
- Description: Logs out a user.
