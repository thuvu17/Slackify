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

import werkzeug.exceptions as wz

import data.songs as songs
import data.users as users
import data.playlists as plists

app = Flask(__name__)
CORS(app)
api = Api(app)
app.secret_key = 'random_test_secret_key'

DELETE = 'delete'
GET = 'get'
DEFAULT = 'Default'
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
USERS_EP = '/users'
SONGS_EP = '/songs'
DEL_USER_EP = f'{USERS_EP}/{DELETE}'
USER_MENU_EP = '/user_menu'
DEL_SONG_EP = f'{SONGS_EP}/{DELETE}'
SONG_MENU_EP = '/song_menu'
PLAYLIST_MENU_EP = '/playlist_menu'
PLAYLISTS_EP = '/playlists'
GET_PLAYLISTS_EP = f'{PLAYLISTS_EP}/{GET}'
DEL_PLAYLIST_EP = f'{PLAYLISTS_EP}/{DELETE}'
SIGN_IN_EP = '/sign_in'
SIGN_UP_EP = '/sign_up'
SIGN_OUT_EP = '/sign_out'


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
@api.route(f'{USER_MENU_EP}/<email>')
class UserMenu(Resource):
    """
    This will deliver our user menu.
    """
    def get(self, email):
        """
        Gets the user menu.
        """
        return {
                   TITLE: USER_MENU_NM,
                   DEFAULT: '0',
                   'Choices': {
                       '1': {
                            'url': '/',
                            'method': 'get',
                            'text': 'Get User Details',
                       },
                       '0': {
                            'text': 'Return',
                       },
                   },
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
    songs.GENRE: fields.String,
    songs.BPM: fields.Integer,
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
        Add a song with provided name, artist, album, genre, bpm.
        """
        name = request.json[songs.NAME]
        artist = request.json[songs.ARTIST]
        album = request.json[songs.ALBUM]
        genre = request.json[songs.GENRE]
        bpm = request.json[songs.BPM]
        new_song = {
            'name': name,
            'artist': artist,
            'album': album,
            'genre': genre,
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
    plists.EMAIL: fields.String,
    plists.NAME: fields.String,
    plists.SONGS: fields.List(fields.String),
})


@api.route(f'{GET_PLAYLISTS_EP}/<email>')
class GetPlaylists(Resource):
    """
    This class lists all playlists belong to a user with given email.
    """
    def get(self, email):
        """
        This method returns all playlists for a user.
        """
        return {
            TYPE: DATA,
            TITLE: f'Current Playlists for {email}',
            DATA: plists.get_playlists(email),
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
        email = request.json[plists.EMAIL]
        name = request.json[plists.NAME]
        try:
            playlist_added = plists.add_playlist(email, name)
            if not playlist_added:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {f'Playlist {name} added': f'{playlist_added}'}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{PLAYLISTS_EP}/<email>/<name>/<new_name>')
class Playlists(Resource):
    """
    Updates the name of a playlist.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def put(self, email, name, new_name):
        """
        Updates the name of a playlist.
        """
        try:
            plists.update_playlist_name(email, name, new_name)
            return {f'Playlist {name}': f'renamed to {new_name}' }
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(f'{DEL_PLAYLIST_EP}/<email>/<name>')
class DelPlaylist(Resource):
    """
    Deletes a playlist by user email and playlist name.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, email, name):
        """
        Deletes a playlist by user_email and playlist name.
        """
        try:
            plists.del_playlist(email, name)
            return {f'Playlist {name}': 'Deleted'}
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
            session[users.EMAIL] = email
            return redirect(f'{USER_MENU_EP}/{email}')
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


@api.route(f'{SIGN_OUT_EP}/<email>')
class SignOut(Resource):
    """
    This class takes care of signing out for users
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    def get(self, email):
        try:
            session.pop(users.EMAIL)
            return "Successfully logged out"
        except KeyError as e:
            raise wz.BadRequest(f'{str(e)}')
