# Slackify
This is a markdown document of details what has already been accomplished in Slackify and set out goals for the upcoming semester.

## Completed Project Summary
### Detail what you have already completed in your project
- Development Environment Working
  - python3, pip3 are installed
  - make dev_env, make tests, ./local.sh, make prod, dev.sh are working
- Github Actions Working
- Makefile configuration improved
- Local + Cloud MongoDB connection to Slackify including 3 databases of songs, users, and playlists
- Local MongoDB Backup
  - bkup.sh: backup the MongoDB in the cloud as JSON files locally
  - restore.sh: restores the JSON backups to local databases
  - common.sh: holds common code for bkup.sh and restore.sh
- Run API Server In the Cloud (on Python Anywhere)
- UI design for frontend completed:
  - Link on Github: https://github.com/thuvu17/slackify/blob/master/doc/design/UI-design-doc.md
- 14 endpoints that are working and well-tested
  - MAIN_MENU_EP: deliver menu page. From menu page, user can go to sign in, sign up
  - USER_MENU_EP: deliver user menu (after logged in). From here, user can go to:
  - their playlist
  - sign_out
  - SIGN_IN: authenticate
  - SIGN_UP: add user
  - SIGN_OUT: pop session (DONE but missing test)
  - USERS_EP
  - SONGS_EP
  - DEL_USER_EP
  - DEL_SONG_EP
  - SONG_MENU_EP
  - PLAYLIST_MENU_EP
  - PLAYLISTS_EP
  - GET_PLAYLIST
  - DEL_PLAYLISTS_EP
- Detailed documentation for each endpoint for Swagger
- Functions and their unit tests
- Code:
  - songs.py: interface to song data
  - users.py: interface to user data
  - playlists.py: interface to playlist data
  - endpoints_song.py: 14 endpoints for flask app
  - get_Spotify_token.py: request to get token from Spotify
  - get_Spotify_playlists.py: request to get playlists from Spotify
  - get_most_popular_songs.py: get top 10 most listened songs on Spotify
  - db_connect.py: connect to MongoDB locally and in the cloud
  - Tests for songs.py, users.py, playlists.py, endpoints_song.py, get_Spotify_token.py, get_Spotify_playlists.py, get_most_popular_songs.py, db_connect.py



### What requirements were met in completing these bits?
- API server created
- A set of data stored in MongoDB
- Project deployment to the cloud
- A dozen or more endpoints
- Each endpoint or function has its own test
- Each endpoint is thoroughly documented for Swagger


## Semester Goals
### Goals
- Auto-deploy server
  - Your server should be auto-deployed by GitHub Actions if all tests pass.
- React Frontend to API server
- HATEOAS feature
  - For example, a pick list (dropdown) that is fetched from the backend.
- Developer endpoint
  - Create at least one endpoint that is useful for developers, and is not intended for end-users  
- Documentation: project proposal, project plans, requirements specification and analysis, design description and implementation
- Basic Features for users:
  - Create playlists based on users’ activity
  - Add/remove songs from playlist
- Recommendation algorithm: 
  - Use machine learning to provide better recommendations (optional)
    - https://youtube.com/shorts/OT_zQpgB7YE?si=oXxe213jzFTBQ7eo

### Detail what the requirement is that each goals will meet & how we expect to meet it
- Update rebuild.sh and deploy.sh and pull in PythonAnywhere to make the server auto-deployed
- Create React frontend based on the UI design we did last semester, [here](doc/design/UI-design-doc.md)
- Connect frontend to the server
- Developer-only endpoints:
  - Endpoints to retrieve all playlists, all songs, and all users
  - Endpoints to delete all songs, all users, and all playlists
- Dropdown list from backend:
- Get API, create a function to manipulate your DOM, pass the data to this function so that it renders the content inside the select tag

