# Slackify
This is a markdown document of details what has already been accomplished in Slackify and set out goals for the upcoming semester.

## Completed Project Summary
1. Detail what you have already completed in your project
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
- UI design for frontend completed: Link on Github: https://github.com/thuvu17/slackify/blob/master/doc/design/UI-design-doc.md
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



2. What requirements were met in completing these bits?

## Semester Goals
1. goals
2. detail what the requirement is that each goals will meet
3. how you expect to meet it.
