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

def create_random_room_code():
    letters = string.ascii_uppercase
    roomNumber=random.choice(letters) + random.choice(letters) + random.choice(letters) + random.choice(letters)
    # TODO: Remove potentially obscene room names
    return roomNumber

class Messager(object):
    """Sends a message to a given user."""

    def __init__(self, unique_id):
        self.unique_id = unique_id

    def CreateChannelToken(self):
        logging.info("Create channel: " + self.unique_id)
        return channel.create_channel(self.unique_id)

    def Send(self, message):
        """Send a message to the client associated with the user."""
        payload = json.dumps(message, default=lambda o: o.__dict__, sort_keys=True)
        logging.info("Sending message to channel %s payload %s" % (self.unique_id, payload))
        channel.send_message(self.unique_id, payload)

class MessageBase(object):
    message_type = 'unknown'

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
        messager = Messager(self.request.get("token"))
        messager.Send(ConnectedMessage())

class IndexHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, None))

class DisplayHandler(webapp2.RequestHandler):
    def post(self):
        # TODO: create a new room
        room = create_random_room_code()
        url = self.request.host_url + "/display/" + room
        logging.info("Redirecting to %s", url)
        return self.redirect(url)

class DisplayRoomHandler(webapp2.RequestHandler):
    def get(self, room_id):
        # TODO: Validate that the room exists
        messager = Messager(room_id + "-unique-token")
        channel_token = messager.CreateChannelToken()
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
        messager = Messager(self.request.get("token"))

        players = []
        for x in range(0, random.randrange(0, 3)):
            players.append(random.choice(["Alex", "Fred", "Emily", "George", "Charles", "Bella"]))

        # HACK - Pick a random name to call it "done"
        if players and players[0] == 'Alex':
            messager.Send(RoomQuestionStatusMessage(room_id))

        messager.Send(RoomWaitingStatusMessage(room_id, players))

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
