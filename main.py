
import datetime
import logging
import os
import random
import json
from google.appengine.api import channel
from google.appengine.api import users
from google.appengine.ext import db
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class Messager(object):
  """Sends a message to a given user."""

  def __init__(self, unique_id):
    self.unique_id = unique_id

  def CreateChannelToken(self):
    logging.info("Create channel: " + self.unique_id)
    return channel.create_channel(self.unique_id)

  def Send(self, message):
    """Send a message to the client associated with the user."""
    channel.send_message(self.unique_id, json.dumps(message))


class ConnectedPage(webapp2.RequestHandler):
  """This page is requested when the client is successfully connected to the channel."""

  def post(self):
    messager = Messager(self.request.get("token"))
    messager.Send("you be connected")

class MainPage(webapp2.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, None))

class DisplayPage(webapp2.RequestHandler):
  def get(self):
    messager = Messager("myuniqueid4444")
    channel_token = messager.CreateChannelToken()
    template_values = { 'channel_token': channel_token }
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

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/display', DisplayPage),
    ('/player', PlayerPage),
    ('/player/([A-Za-z]+)', PlayerRoomPage),
    #('/setname', SetNamePage),
    ('/connected', ConnectedPage)
    ], debug=True)


def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
