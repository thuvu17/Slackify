"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.

Please review the documentation for endpoints on
https://github.com/thuvu17/slackify/blob/master/doc/design/slackify-endpoint.md
"""
from http import HTTPStatus

from flask import Flask, request, redirect, session
from flask_restx import Resource, Api, fields
from flask_cors import CORS
import pymongo as pm
from pymongo.errors import ConnectionFailure

import werkzeug.exceptions as wz

import data.songs as songs
import data.users as users
import data.playlists as plists
import form.form as form
import data.recommend as rec
import data.get_Spotify_token as get_spotify_token

app = Flask(__name__)
CORS(app)
api = Api(app)
app.secret_key = 'random_test_secret_key'

DELETE = 'delete'
GET = 'get'
DEFAULT = 'Default'
UPDATE = 'Update'
MENU = 'menu'
SONG_ID = 'Song ID'
TYPE = 'Type'
DATA = 'Data'
TITLE = 'Title'
RETURN = 'Return'

# EP names
MAIN_MENU_NM = "Welcome to Slackify!"
USER_MENU_NM = 'User Menu'
SONG_MENU_NM = 'Song Menu'
PLAYLIST_MENU_NM = 'Playlist Menu'
HELLO_RESP = 'hello'

# Endpoints
HELLO_EP = '/hello'
MAIN_MENU_EP = '/MainMenu'
FORM_EP = '/form'
USERS_EP = '/users'
SONGS_EP = '/songs'
TOKEN_EP = '/token'
DEL_USER_EP = f'{USERS_EP}/{DELETE}'
USER_MENU_EP = '/user_menu'
DEL_SONG_EP = f'{SONGS_EP}/{DELETE}'
SONG_MENU_EP = '/song_menu'
PLAYLIST_MENU_EP = '/playlist_menu'
PLAYLISTS_EP = '/playlists'
GET_PLAYLISTS_EP = f'{PLAYLISTS_EP}/{GET}'
DEL_PLAYLIST_EP = f'{PLAYLISTS_EP}/{DELETE}'
UPDATE_PLAYLIST_EP = f'{PLAYLISTS_EP}/{UPDATE}'
PLAYLIST_EP = '/playlist'
ADD_SONG_PLAYLIST_EP = f'{PLAYLIST_EP}/{UPDATE}'
SIGN_IN_EP = '/sign_in'
SIGN_UP_EP = '/sign_up'
SIGN_OUT_EP = '/sign_out'
SONG_REC_EP = '/rec'
SONG_REC_AVG_STRIDE_EP = f'{SONG_REC_EP}/avg_stride'    # avg stride length
SONG_REC_STRIDE_EP = f'{SONG_REC_EP}/stride'       # provided stride length
SONG_REC_HEIGHT_EP = f'{SONG_REC_EP}/height'


@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO_RESP: 'world'}


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(f'{MAIN_MENU_EP}')
class MainMenu(Resource):
    """
    This will deliver our main menu.
    """
    def get(self):
        """
        Gets the main menu.
        """
        return {TITLE: MAIN_MENU_NM,
                DEFAULT: 2,
                'Choices': {
                    '1': {'url': f'{SIGN_IN_EP}',
                          'method': 'get', 'text': 'Sign in'},
                    '2': {'url': f'{SIGN_UP_EP}',
                          'method': 'get', 'text': 'Sign up'},
                    '3': {'url': f'{SONGS_EP}',
                          'method': 'get', 'text': 'List Songs'},
                    '4': {'url': '/',
                          'method': 'get', 'text': 'Illustrating a Point!'},
                    'X': {'text': 'Exit'},
                }}


# ---------------- USER EPS -----------------
@api.route(f'{USER_MENU_EP}/<user_id>')
class UserMenu(Resource):
    """
    This will deliver our user menu.
    """
    def get(self, user_id):
        """
        Gets the user menu.
        """
        user_data = users.get_user_info(user_id)
        print(user_data)
        return {
                   TITLE: USER_MENU_NM,
                   users.ID: user_data[users.ID],
                   users.NAME: user_data[users.NAME],
                   users.EMAIL: user_data[users.EMAIL],
                   users.PASSWORD: user_data[users.PASSWORD],
               }


user_fields = api.model('NewUser', {
    users.NAME: fields.String,
    users.EMAIL: fields.String,
    users.PASSWORD: fields.String,
})


@api.route(f'{USERS_EP}')
class Users(Resource):
    """
    This class supports fetching a list of all users.
    """
    def get(self):
        """
        This method returns all users.
        """
        return {
           TYPE: DATA,
           TITLE: 'Current Users',
           DATA: users.get_users(),
           RETURN: MAIN_MENU_EP,
        }

    @api.expect(user_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a user with provided name, email, password.
        """
        name = request.json[users.NAME]
        email = request.json[users.EMAIL]
        password = request.json[users.PASSWORD]
        new_user = {
            'name': name,
            'email': email,
            'password': password,
        }
        try:
            user_added = users.add_user(new_user)
            if not user_added:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {'User added': f'{user_added}'}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{DEL_USER_EP}/<email>')
class DelUser(Resource):
    """
    Deletes a user by email.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, email):
        """
        Deletes a user by name and artist.
        """
        try:
            users.del_user(email)
            return {'User with email ' + f'{email}': 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


# ---------------- SONG EPS -----------------
song_fields = api.model('NewSong', {
    songs.NAME: fields.String,
    songs.ARTIST: fields.String,
    songs.ALBUM: fields.String,
    songs.BPM: fields.Integer,
    songs.ENERGY: fields.Integer,
})


@api.route(f'{SONGS_EP}')
class Songs(Resource):
    """
    This class supports listing and adding a song.
    """
    def get(self):
        """
        This method returns all songs.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current Songs',
            DATA: songs.get_songs(),
            MENU: SONG_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(song_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a song with provided name, artist, album, engergy, bpm.
        """
        name = request.json[songs.NAME]
        artist = request.json[songs.ARTIST]
        album = request.json[songs.ALBUM]
        energy = request.json[songs.ENERGY]
        bpm = request.json[songs.BPM]
        new_song = {
            'name': name,
            'artist': artist,
            'album': album,
            'energy': energy,
            'bpm': bpm,
        }
        try:
            song_added = songs.add_song(new_song)
            if not song_added:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {'Song added': f'{song_added}'}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{DEL_SONG_EP}/<name>/<artist>')
class DelSong(Resource):
    """
    Deletes a song by name and artist.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, name, artist):
        """
        Deletes a song by name and artist.
        """
        try:
            songs.del_song(name, artist)
            return {name: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


# ---------------- PLAYLIST EPS -----------------
playlist_fields = api.model('NewPlaylist', {
    plists.USER_ID: fields.String,
    plists.NAME: fields.String,
})


@api.route(f'{GET_PLAYLISTS_EP}/<user_id>')
class GetPlaylists(Resource):
    """
    This class lists all playlists belong to a user with given email.
    """
    def get(self, user_id):
        """
        This method returns all playlists for a user.
        """
        return {
            TYPE: DATA,
            TITLE: f'Current Playlists for {user_id}',
            DATA: plists.get_playlists(user_id),
            MENU: PLAYLIST_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }


@api.route(f'{GET_PLAYLISTS_EP}')
class GetAllPlaylists(Resource):
    """
    This class lists all playlists.
    """
    def get(self):
        """
        This method returns all playlists.
        """
        return {
            TYPE: DATA,
            TITLE: 'Current Playlists',
            DATA: plists.get_all_playlists(),
            MENU: PLAYLIST_MENU_EP,
            RETURN: MAIN_MENU_EP,
        }


@api.route(f'{PLAYLISTS_EP}')
class Playlists(Resource):
    """
    This class supports various operations on playlists, such as
    listing them, and creating a playlist.
    """
    @api.expect(playlist_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a playlist.
        """
        user_id = request.json[plists.USER_ID]
        name = request.json[plists.NAME]
        try:
            playlist_added = plists.add_playlist(user_id, name)
            if not playlist_added:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {f'Playlist {name} added': f'{playlist_added}'}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{DEL_PLAYLIST_EP}/<user_id>/<name>')
class DelPlaylist(Resource):
    """
    Deletes a playlist by user id and playlist name.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, user_id, name):
        """
        Deletes a playlist by user id and playlist name.
        """
        try:
            plists.del_playlist(user_id, name)
            return {f'Playlist {name}': 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(f'{UPDATE_PLAYLIST_EP}/<user_id>/<name>/<new_name>')
class PlaylistsName(Resource):
    """
    Updates the name of a playlist.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def put(self, user_id, name, new_name):
        """
        Updates the name of a playlist.
        """
        try:
            plists.update_playlist_name(user_id, name, new_name)
            return {f'Playlist {name}': f'renamed to {new_name}'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(f'{PLAYLIST_EP}/<user_id>/<name>')
class PlaylistSongs(Resource):
    """
    Get all songs in a playlist.
    """
    def get(self, user_id, name):
        """
        Get all songs in a playlist.
        """
        try:
            return {
                TYPE: DATA,
                TITLE: f'Current Songs for Playlist {name} by {user_id}',
                DATA: plists.playlist_get_all_song(user_id, name),
                MENU: PLAYLIST_MENU_EP,
                RETURN: MAIN_MENU_EP,
            }
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(f'{ADD_SONG_PLAYLIST_EP}/<user_id>/<name>/<song_id>')
class PlaylistAddSong(Resource):
    """
    Add a song to a playlist.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def put(self, user_id, name, song_id):
        """
        Updates the songs of a playlist.
        """
        try:
            plists.update_add_songs_in_playlist(user_id, name, song_id)
            return {f'Song {song_id}': f'added to playlist {name}'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


# ---------------- AUTH EPS -----------------
@api.route(f'{SIGN_IN_EP}/<email>/<password>')
class SignIn(Resource):
    """
    This class takes care of signing in for users
    """
    @api.response(HTTPStatus.FOUND, 'Found')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized')
    def get(self, email, password):
        try:
            valid_user = users.auth_user(email, password)
            if not valid_user:
                raise wz.Unauthorized('Invalid credentials')
            user_id = users.get_id(email, password)
            session[users.ID] = user_id
            return redirect(f'{USER_MENU_EP}/{user_id}')
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{SIGN_UP_EP}/<email>/<password>/<username>')
class SignUp(Resource):
    """
    This class takes care of signing up for users
    """
    @api.response(HTTPStatus.FOUND, 'New user added')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    def get(self, email, password, username):
        new_user = {
            users.EMAIL: email,
            users.PASSWORD: password,
            users.NAME: username,
        }
        try:
            valid_new_user = users.add_user(new_user)
            if not valid_new_user:
                raise wz.BadRequest()
            return redirect(f'{USER_MENU_EP}/{email}')
        except ValueError as e:
            raise wz.BadRequest(f'{str(e)}')


@api.route(f'{SIGN_OUT_EP}')
class SignOut(Resource):
    """
    This class takes care of signing out for users
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    def get(self):
        try:
            if users.ID not in session:
                return "User is not logged in", HTTPStatus.BAD_REQUEST
            session.pop(users.ID)
            if users.ID in session:
                return "User was not logged out properly",
            HTTPStatus.INTERNAL_SERVER_ERROR

            return "Successfully logged out", HTTPStatus.OK

        except KeyError as e:
            raise wz.BadRequest(f'{str(e)}')


# ---------------- FORM EP ------------------
@api.route(FORM_EP)
class Form(Resource):
    """
    This class is for form
    """
    def get(self):
        form_descr = form.get_form_descr()
        field_names = form.get_fld_names()
        return {
            'form_description': form_descr,
            'field_names': field_names,
        }


# -------------- RECOMMENDATION EPS -----------------
@api.route(f'{SONG_REC_AVG_STRIDE_EP}/<speed>/<gender>')
class RecommendSongFromAvgStride(Resource):
    def get(self, speed, gender):
        rec_bpm = rec.get_bpm_from_speed_avg_stride(speed, gender)
        return rec.rec_song_from_bpm(rec_bpm)


# -------------------- TOKEN EPS -----------------------
@api.route(f'{TOKEN_EP}')
class Token(Resource):
    """
    This class supports functionalities token-related
    """
    def get(self):
        """
        This method returns a Spotify token
        """
        return get_spotify_token.get_token()


# -------------------- DEV EPS -----------------------
@api.route('/dev/check-mongodb-connection')
class CheckMongoDBConnection(Resource):
    """
    This class provides functionality to check the MongoDB connection.
    """
    def get(self):
        """
        Checks the MongoDB connection and returns the status.
        """
        try:
            client = client = pm.MongoClient()
            db = client["slackifyDB"]
            db.list_collection_names()
            client.close()
            return {"status": "Connection to MongoDB successful."}
        except ConnectionFailure:
            return {"status": "Failed to connect to MongoDB."}
