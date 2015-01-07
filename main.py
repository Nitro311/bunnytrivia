import datetime
import logging
import json
import os
import random
import time
import string
import uuid
import webapp2
from google.appengine.api import channel
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from questions import questions

DEBUG = False

if os.environ.get('SERVER_SOFTWARE','').startswith('Development'):
    DEBUG = True

class UserState(object):
    def __init__(self, nickname, is_ready):
        self.nickname = nickname
        self.is_ready = is_ready

class Room(object):
    def __init__(self):
        self.room_id = self.create_random_id()
        self.status = "waiting"
        self.user_ids = []

    def upsert_user(self, user_id):
        if not user_id in self.user_ids:
            self.user_ids.append(user_id)

    def create_random_id(self):
        letters = string.ascii_uppercase
        result = random.choice(letters) + random.choice(letters) + random.choice(letters) + random.choice(letters)
        # TODO: Remove potentially obscene room names
        return result

    def get_state(self):
        users = [User.load(user_id) for user_id in self.user_ids]
        return dict(status = self.status, users = [UserState(user.nickname, user.is_ready) for user in users])

    @staticmethod
    def load(room_id):
        return memcache.get("room-" + room_id)

    def save(self):
        memcache.set("room-" + self.room_id, self)

class User(object):
    def __init__(self):
        self.user_id = self.create_random_id()
        self.token = ''
        self.nickname = ''
        self.score = 0
        self.is_ready = False;

    def create_random_id(self):
        letters = string.ascii_lowercase
        result = random.choice(letters) + random.choice(letters) + random.choice(letters) + random.choice(letters)
        return result
        # TODO: Return to using GUIDs after testing
        #return str(uuid.uuid4())

    @staticmethod
    def load(user_id):
        return memcache.get("user-" + user_id)

    def save(self):
        memcache.set("user-" + self.user_id, self)

class RoomMessenger(object):
    """Sends a message to all users within the given room."""

    def __init__(self, room_id):
        self.room_id = room_id

    def send(self, message):
        logging.info("Sending message to room " + self.room_id)
        room = Room.load(self.room_id)
        for user_id in room.user_ids:
            messager = UserMessenger(user_id)
            messager.send(message)

class UserMessenger(object):
    """Sends a message to a given user."""

    def __init__(self, user_id):
        self.user_id = user_id

    def create_channel_token(self):
        logging.info("Create channel: " + self.user_id)
        return channel.create_channel(self.user_id)

    def send(self, message):
        payload = json.dumps(message, default=lambda o: o.__dict__, sort_keys=True)
        logging.info("Sending message to channel %s payload %s" % (self.user_id, payload))
        channel.send_message(self.user_id, payload)


class ConnectedMessage(object):
    def __init__(self):
        self.message_type = 'connected'

class NewNicknameMessage(object):
    def __init__(self, newnickname):
        self.message_type = 'newnickname'
        self.newnickname = newnickname

class RoomWaitingStateMessage(object):
    def __init__(self, room_id, room_state):
        self.message_type = "room"
        self.room_id = room_id
        self.room = room_state

class RoomQuestionStateMessage(object):
    def __init__(self, room_id):
        self.message_type = "room"
        self.status = "question"
        self.question = temporary_question


class BaseRoomHandler(webapp2.RequestHandler):
    def get_room_user_token(self, room_id):
        room = Room.load(room_id)

        user_id = self.request.cookies.get("user_id")
        logging.info("user_id from cookies:" + str(user_id))
        user = None

        if user_id:
            user = User.load(user_id)
            logging.info("loaded user from user_id:" + str(user))

        if not user:
            user = User()
            user_id = user.user_id
            user.save()

        logging.info("room, user, token: (%s, %s, %s)" % (room, user, self.request.get("token")))
        return (room, user, self.request.get("token"))

class IndexHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, None))


class RoomConnectHandler(BaseRoomHandler):
    def post(self, room_id):
        room_id = room_id.upper()
        (room, user, token) = self.get_room_user_token(room_id)
        logging.info("Room state requested for %s by %s" % (room_id, token))

        if not room:
            logging.warn("Room does not exist")
            return

        room.upsert_user(user.user_id)
        room.save()

        messenger = UserMessenger(user.user_id)
        messenger.send(ConnectedMessage())

        if DEBUG:
            time.sleep(0.5)

        messenger = RoomMessenger(room.room_id)
        messenger.send(RoomWaitingStateMessage(room_id, room.get_state()))

class RoomSetNicknameHandler(BaseRoomHandler):
    def post(self, room_id):
        room_id = room_id.upper()
        (room, user, token) = self.get_room_user_token(room_id)
        newnickname = self.request.get('newnickname').upper()
        logging.info("Renaming user %s to %s" % (user.nickname, newnickname))

        if not room:
            logging.warn("Room does not exist")
            return

        #TODO: Verify change

        user.nickname = newnickname
        user.save()

        messenger = UserMessenger(user.user_id)
        messenger.send(NewNicknameMessage(user.nickname))

        messenger = RoomMessenger(room.room_id)
        messenger.send(RoomWaitingStateMessage(room_id, room.get_state()))

class RoomStartHandler(webapp2.RequestHandler):
    def post(self):
        room = Room()
        url = self.request.host_url + "/room/" + room.room_id
        logging.info("Redirecting to %s", url)
        return self.redirect(url)

class RoomViewHandler(BaseRoomHandler):
    def get(self, room_id):
        room_id = room_id.upper()
        (room, user, token) = self.get_room_user_token(room_id)

        if not room:
            # TODO: Redirect them back to room creation instead of creating a new room
            room = Room()
            room.room_id = room_id
            room.save()

        logging.info("Creating channel for %s id: %s" % (user, user.user_id))
        messenger = UserMessenger(user.user_id)
        channel_token = messenger.create_channel_token()
        template_values = { 'channel_token': channel_token, 'user_id': user.user_id, 'room_id': room.room_id, 'nickname': user.nickname }
        path = os.path.join(os.path.dirname(__file__), 'room.html')
        user_id = self.request.cookies.get("user_id")
        if not user_id or user.user_id != user_id:
            self.response.set_cookie('user_id', user.user_id, max_age=60 * 60 * 24, path='/room/' + room.room_id, overwrite=True)
        self.response.out.write(template.render(path, template_values))

class RoomStateHandler(BaseRoomHandler):
    def post(self, room_id):
        room_id = room_id.upper()
        logging.info("Room state requested for %s by %s" % (room_id, self.request.get("token")))
        room = Room.load(room_id)
        if not room:
            return

        messenger = UserMessenger(self.request.get("token"))
        messenger.send(RoomWaitingStateMessage(room_id, room.get_state()))


temporary_question = random.choice(questions).question

app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/room/?', RoomStartHandler),
    ('/room/([A-Za-z]+)', RoomViewHandler),
    ('/room/([A-Za-z]+)/connect', RoomConnectHandler),
    ('/room/([A-Za-z]+)/state', RoomStateHandler),
    ('/room/([A-Za-z]+)/setnickname', RoomSetNicknameHandler)
    ], debug=True)
