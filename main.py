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

class DateTimeJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        self.sort_keys = True
        if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
            return obj.isoformat()[:-3] + "Z"
        else:
            return obj.__dict__

class UserState(object):
    def __init__(self, nickname, is_ready):
        self.nickname = nickname
        self.is_ready = is_ready

    def __str__(self):
        return '<%s: %s>' % (self.__class__.__name__, json.dumps(self, cls=DateTimeJSONEncoder))

class Room(object):
    def __init__(self):
        self.round=1
        self.room_id = self.create_random_id()
        self.status = "waiting"
        self.user_ids = []
        self.question = None
        self.guesses = {}
        self.host = None
        self.time_to_switch = None

    def set_guess(self, user_id, guess):
        if self.status == 'questionguess':
            self.guesses[user_id] = guess

    def start_game(self):
        self.status = "round"
        self.round = 1
        self.time_to_switch = datetime.datetime.now() + datetime.timedelta(0,5)

    def upsert_user(self, user_id):
        if not user_id in self.user_ids:
            self.user_ids.append(user_id)

    def advance_state(self):
        if self.time_to_switch < datetime.datetime.now():
            if self.status == "round":
                self.status = "questionguess"
                self.time_to_switch = datetime.datetime.now() + datetime.timedelta(0,5)
                self.guesses = {}
                self.question = random.choice(questions)
                self.save()
            elif self.status == "questionguess":
                self.status = "questionanswer"
                self.time_to_switch = datetime.datetime.now() + datetime.timedelta(0,5)
                self.save()
            elif self.status == "questionanswer":
                self.status = "questionreveal"
                self.time_to_switch = datetime.datetime.now() + datetime.timedelta(0,5)
                self.save()
            elif self.status == "questionreveal":
                self.status = "questionscore"
                self.time_to_switch = datetime.datetime.now() + datetime.timedelta(0,5)
                self.save()
            elif self.status == "questionscore":
                self.status = "score"
                self.time_to_switch  =datetime.datetime.now()+datetime.timedelta(0,5)
                self.save()
            elif self.status == "score":
                self.status = "round"
                self.round = self.round + 1
                self.time_to_switch = datetime.datetime.now() + datetime.timedelta(0,5)
                self.save()
    def create_random_id(self):
        letters = string.ascii_uppercase
        result = random.choice(letters) + random.choice(letters) + random.choice(letters) + random.choice(letters)
        # TODO: Remove potentially obscene room names
        return result

    @staticmethod
    def load(room_id):
        return memcache.get("room-" + room_id)

    def save(self):
        # HACK: Not sure we we actually need to reset the host here
        self.host = self.user_ids[0] if len(self.user_ids) > 0 else None
        memcache.set("room-" + self.room_id, self)

    def __str__(self):
        return '<%s: %s>' % (self.__class__.__name__, json.dumps(self, cls=DateTimeJSONEncoder))

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

    def __str__(self):
        return '<%s: %s>' % (self.__class__.__name__, json.dumps(self, cls=DateTimeJSONEncoder))


class ConnectedMessage(object):
    def __init__(self):
        self.message_type = 'connected'

class NewNicknameMessage(object):
    def __init__(self, newnickname):
        self.message_type = 'newnickname'
        self.newnickname = newnickname

class RoomStateMessage(object):
    def __init__(self, room):
        self.message_type = "room"
        self.room_id = room.room_id
        self.room = self.get_state(room)

    def get_state(self,room):
        users = [User.load(user_id) for user_id in room.user_ids]
        switch_interval = (room.time_to_switch - datetime.datetime.now()).total_seconds() * 1000.0 if room.time_to_switch else None

        if room.status == 'waiting':
            return dict(
                room_id = room.room_id,
                status = room.status,
                users = [UserState(user.nickname, user.is_ready) for user in users],
            )
        elif room.status == "round":
            return dict(
                room_id = room.room_id,
                status = room.status,
                round = room.round,
                time_to_switch = room.time_to_switch,
                switch_interval = switch_interval
            )
        elif room.status == "questionguess":
            return dict(
                room_id = room.room_id,
                status = room.status,
                question = room.question.question,
                time_to_switch = room.time_to_switch,
                switch_interval = switch_interval
            )
        elif room.status == "questionanswer":
            return dict(
                room_id = room.room_id,
                status = room.status,
                guesses = ['TODO', 'LATER', 'Ill get er done'],
                question = room.question.question,
                time_to_switch = room.time_to_switch,
                switch_interval = switch_interval
            )
        elif room.status == "questionreveal":
            return dict(
                room_id = room.room_id,
                status = room.status,
                guesses = [dict(answer=room.question.answer, guesssers=room.user_ids, is_correct=True)],
                question = room.question.question,
                time_to_switch = room.time_to_switch,
                switch_interval = switch_interval
            )
        elif room.status == "questionscore":
            return dict(
                room_id = room.room_id,
                status = room.status,
                users = [UserState(user.nickname, user.is_ready) for user in users],
                question = room.question.question,
                time_to_switch = room.time_to_switch,
                switch_interval = switch_interval
            )
        elif room.status == "score":
            return dict(
                room_id = room.room_id,
                status = room.status,
                users = [UserState(user.nickname, user.is_ready) for user in users],
                time_to_switch = room.time_to_switch,
                switch_interval = switch_interval
            )

            #answerers = self.guesses.keys() if self.guesses else [],
            #guesses = [dict(nickname = user.nickname, guess = self.guesses[user.user_id]) for user in users] if self.status == "answeredquestion" and self.guesses else None



class BaseRoomHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.messages = {}

    def add_user_message(self, user_id, message):
        logging.info("Adding message to user " + user_id)
        if user_id in self.messages:
            self.messages[user_id].append(message)
        else:
            self.messages[user_id] = [message]

    def add_room_message(self, room_id, message):
        logging.info("Sending message to room " + room_id)
        room = Room.load(room_id)
        for user_id in room.user_ids:
            self.add_user_message(user_id, message)

    def send_messages(self):
        for user_id in self.messages:
            messages_to_send = self.messages[user_id]
            payload = json.dumps(messages_to_send, cls=DateTimeJSONEncoder)
            logging.info("Sending %d messages to %s" % (len(messages_to_send), user_id))
            channel.send_message(user_id, payload)

    def create_channel_token(self, user_id):
        logging.info("Create channel: " + user_id)
        return channel.create_channel(user_id)

    def get_room_and_user(self, room_id):
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

        logging.info("room, user: (%s, %s)" % (room, user))
        return (room, user)

class IndexHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        if (self.request.get("reason") == "room_not_found"):
                template_values = { "alert": "The room was not found"}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class RoomCheckStateHandler(BaseRoomHandler):
    def post(self, room_id):
        room_id = room_id.upper()
        (room, user) = self.get_room_and_user(room_id)
        logging.info("Room state check requested for %s by %s" % (room_id, user.user_id))

        if not room:
            logging.warn("Room does not exist")
            return

        if room.host == user.user_id:
            logging.info("Advancing the room state")
            room.advance_state()
            self.add_room_message(room.room_id, RoomStateMessage(room))
            self.send_messages()

        else:
            logging.warn('Did not advance the room state because user %s is not host %s' % (user.user_id, room.host))



class RoomConnectHandler(BaseRoomHandler):
    def post(self, room_id):
        room_id = room_id.upper()
        (room, user) = self.get_room_and_user(room_id)
        logging.info("Room state requested for %s by %s" % (room_id, user.user_id))

        if not room:
            logging.warn("Room does not exist")
            return

        room.upsert_user(user.user_id)
        room.save()

        self.add_user_message(user.user_id, ConnectedMessage())
        self.add_room_message(room.room_id, RoomStateMessage(room))
        self.send_messages()

class RoomSetNicknameHandler(BaseRoomHandler):
    def post(self, room_id):
        room_id = room_id.upper()
        (room, user) = self.get_room_and_user(room_id)
        newnickname = self.request.get('newnickname').upper()
        logging.info("Renaming user %s to %s" % (user.nickname, newnickname))

        if not room:
            logging.warn("Room does not exist")
            return

        #TODO: Verify change

        user.nickname = newnickname
        user.save()

        self.add_user_message(user.user_id, NewNicknameMessage(user.nickname))
        self.add_room_message(room.room_id, RoomStateMessage(room))
        self.send_messages()

class RoomCreateHandler(webapp2.RequestHandler):
    def post(self):
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

        room = Room()
        # TODO: Figure out why the host doesn't get set right
        room.host =  user.user_id
        room.save()
        url = self.request.host_url + "/room/" + room.room_id
        logging.info("Redirecting to %s", url)
        return self.redirect(url)

class RoomViewHandler(BaseRoomHandler):
    def get(self, room_id):
        room_id = room_id.upper()
        (room, user) = self.get_room_and_user(room_id)

        if not room:
            url = self.request.host_url + "?reason=room_not_found"
            return self.redirect(url)

        logging.info("Creating channel for %s id: %s" % (user, user.user_id))
        channel_token = self.create_channel_token(user.user_id)
        template_values = { 'channel_token': channel_token, 'user_id': user.user_id, 'room_id': room.room_id, 'nickname': user.nickname }
        path = os.path.join(os.path.dirname(__file__), 'room.html')
        user_id = self.request.cookies.get("user_id")
        if not user_id or user.user_id != user_id:
            self.response.set_cookie('user_id', user.user_id, max_age=60 * 60 * 24, overwrite=True)
        self.response.out.write(template.render(path, template_values))

class RoomStartGameHandler(BaseRoomHandler):
    def post(self, room_id):
        room_id = room_id.upper()
        (room, user) = self.get_room_and_user(room_id)
        logging.info("Game start requested for %s by %s" % (room_id, user.user_id))

        if not room:
            logging.warn("Room does not exist")
            return

        room.start_game()
        room.save()

        self.add_room_message(room.room_id, RoomStateMessage(room))
        self.send_messages()

class RoomSendGuessHandler(BaseRoomHandler):
    def post(self, room_id):
        room_id = room_id.upper()
        (room, user) = self.get_room_and_user(room_id)
        guess = self.request.get('guess').upper()
        logging.info("Guess %s received %s by %s" % (guess,room_id, user.user_id))


        if not room:
            logging.warn("Room does not exist")
            return

        room.set_guess(user.user_id, guess)
        room.save()

        self.add_room_message(room.room_id, RoomStateMessage(room))
        self.send_messages()


app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/room/?', RoomCreateHandler),
    ('/room/([A-Za-z]+)', RoomViewHandler),
    ('/room/([A-Za-z]+)/checkstate', RoomCheckStateHandler),
    ('/room/([A-Za-z]+)/connect', RoomConnectHandler),
    ('/room/([A-Za-z]+)/sendguess', RoomSendGuessHandler),
    ('/room/([A-Za-z]+)/setnickname', RoomSetNicknameHandler),
    ('/room/([A-Za-z]+)/startgame', RoomStartGameHandler)
    ], debug=True)
