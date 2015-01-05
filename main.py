
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

def getRoomNumber():
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


class ConnectedPage(webapp2.RequestHandler):
    """This page is requested when the client is successfully connected to the channel."""

    def post(self):
        messager = Messager(self.request.get("token"))
        messager.Send(dict(message_type = "connected"))

class MainPage(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, None))

class DisplayPage(webapp2.RequestHandler):
    def get(self):
        # TODO: create a new room
        room = getRoomNumber()
        url = self.request.host_url + "/display/" + room
        logging.info("Redirecting to %s", url)
        return self.redirect(url)

class DisplayRoomPage(webapp2.RequestHandler):
    def get(self, room):
        # TODO: Validate that the room exists
        messager = Messager(room + "-unique-token")
        channel_token = messager.CreateChannelToken()
        template_values = { 'channel_token': channel_token, 'room': room.upper() }
        path = os.path.join(os.path.dirname(__file__), 'display.html')
        self.response.out.write(template.render(path, template_values))

class PlayerPage(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'player.html')
        self.response.out.write(template.render(path, None))

class PlayerRoomPage(webapp2.RequestHandler):
    def get(self, room):
        template_values = { 'room': room.upper() }
        path = os.path.join(os.path.dirname(__file__), 'player.html')
        self.response.out.write(template.render(path, template_values))


class RoomHandler(webapp2.RequestHandler):
    def post(self, room):
        logging.info("Room status requested for %s by %s" % (room, self.request.get("token")))
        messager = Messager(self.request.get("token"))
        messager.Send(GetRoomStatus(room))

def GetRoomStatus(room):
    return RoomStatus(room)

class RoomStatus(object):
    def __init__(self, room_id):
        self.message_type = "room"
        self.room_id = room_id
        self.players = []
        for x in range(0, random.randrange(0, 3)):
            self.players.append(random.choice(["Alex", "Fred", "Emily", "George", "Charles", "Bella"]))
        self.status = "waiting"

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/display/?', DisplayPage),
    ('/display/([A-Za-z]+)', DisplayRoomPage),
    ('/player/?', PlayerPage),
    ('/player/([A-Za-z]+)', PlayerRoomPage),
    ('/api/room/([A-Za-z]+)', RoomHandler),
    #('/setname', SetNamePage),
    ('/connected', ConnectedPage)
    ], debug=True)
