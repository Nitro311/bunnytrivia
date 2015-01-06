import datetime
import logging
import os
import random
import json
import string
from google.appengine.api import channel
from google.appengine.api import users
from google.appengine.ext import db
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from questions import questions


class Room(object):
    def __init__(self, room_id = None):
        if not room_id:
            self.room_id = self.create_random_room_id()
            # TODO: Any other initialization
        else:
            self.room_id = room_id
            # TODO: load from memcache

    def create_random_room_id(self):
        letters = string.ascii_uppercase
        result = random.choice(letters) + random.choice(letters) + random.choice(letters) + random.choice(letters)
        # TODO: Remove potentially obscene room names
        return result

    def save(self):
        # TODO: Save to memcache
        pass

class User(object):
    def __init__(self, user_id = None):
        if not user_id:
            # TODO: Create user id
            user_id = "RANDOM ID"
        self.user_id = user_id

    def save(self):
        # TODO: Save to memcache
        pass

class RoomBroadcaster(object):
    """Sends a message to all users within the given room."""

    def __init__(self, room_id, sending_user_id):
        self.room_id = room_id
        self.sending_user_id = sending_user_id

    def send(self, message):
        """Send the given message to all users in the given room."""

        # TODO: Figure out how to get the users in the room
        users_in_room = []
        for user in users_in_room:
            if (self.sending_user_id is None or user.user_id != self.sending_user_id):
              messager = UserMessenger(user.user_id)
              messager.send(message)

class UserMessenger(object):
    """Sends a message to a given user."""

    def __init__(self, user_id):
        self.user_id = user_id

    def create_channel_token(self):
        logging.info("Create channel: " + self.user_id)
        return channel.create_channel(self.user_id)

    def send(self, message):
        """Send a message to the client associated with the user."""
        payload = json.dumps(message, default=lambda o: o.__dict__, sort_keys=True)
        logging.info("Sending message to channel %s payload %s" % (self.user_id, payload))
        channel.send_message(self.user_id, payload)

class MessageBase(object):
    def __init__(self):
        self.message_type = 'unknown'

class ConnectedMessage(MessageBase):
    def __init__(self):
        self.message_type = 'connected'

class RoomWaitingStatusMessage(MessageBase):
    def __init__(self, room_id, players):
        self.message_type = "room"
        self.room_id = room_id
        self.players = players
        self.status = "waiting"

class RoomQuestionStatusMessage(MessageBase):
    def __init__(self, room_id):
        self.message_type = "room"
        self.status = "question"
        self.question = temporary_question


class ApiConnectHandler(webapp2.RequestHandler):
    """This page is requested when the client is successfully connected to the channel."""

    def post(self):
        messenger = UserMessenger(self.request.get("token"))
        messenger.send(ConnectedMessage())

class IndexHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, None))

class DisplayHandler(webapp2.RequestHandler):
    def post(self):
        room = Room()
        url = self.request.host_url + "/display/" + room.room_id
        logging.info("Redirecting to %s", url)
        room.save()
        return self.redirect(url)

class DisplayRoomHandler(webapp2.RequestHandler):
    def get(self, room_id):
        # TODO: Validate that the room exists
        messenger = UserMessenger(room_id + "-unique-token")
        channel_token = messenger.create_channel_token()
        template_values = { 'channel_token': channel_token, 'room': room_id.upper() }
        path = os.path.join(os.path.dirname(__file__), 'display.html')
        self.response.out.write(template.render(path, template_values))

class PlayerHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'player.html')
        self.response.out.write(template.render(path, None))

class PlayerRoomHandler(webapp2.RequestHandler):
    def get(self, room_id):
        template_values = { 'room': room_id.upper() }
        path = os.path.join(os.path.dirname(__file__), 'player.html')
        self.response.out.write(template.render(path, template_values))

class ApiRoomHandler(webapp2.RequestHandler):
    def post(self, room_id):
        logging.info("Room status requested for %s by %s" % (room_id, self.request.get("token")))
        messenger = UserMessenger(self.request.get("token"))

        players = []
        for x in range(0, random.randrange(0, 3)):
            players.append(random.choice(["Alex", "Fred", "Emily", "George", "Charles", "Bella"]))

        # HACK - Pick a random name to call it "done"
        if players and players[0] == 'Alex':
            messenger.send(RoomQuestionStatusMessage(room_id))

        messenger.send(RoomWaitingStatusMessage(room_id, players))

# TODO: Fake this all in memory!

temporary_question = random.choice(questions).question

app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/display/?', DisplayHandler),
    ('/display/([A-Za-z]+)', DisplayRoomHandler),
    ('/player/?', PlayerHandler),
    ('/player/([A-Za-z]+)', PlayerRoomHandler),

    ('/api', ApiConnectHandler),
    ('/api/room/([A-Za-z]+)', ApiRoomHandler)
    ], debug=True)
