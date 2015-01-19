import datetime
import logging
import json
import os
import random
import time
import string
import uuid
import webapp2
from types import GeneratorType
from google.appengine.api import channel
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models.dbquestion import DbQuestion, DbAnswer, import_questions_if_needed, export_questions, delete_all_questions
from models.dbnewquestion import DbNewQuestion
from wordfixer import WordFixer

class DateTimeJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        self.sort_keys = True
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()[:-3] + "Z"
        if isinstance(obj, (set, GeneratorType)):
            return list(obj)
        else:
            return obj.__dict__

class Room(object):
    timedelta_for_information = datetime.timedelta(0, 5)
    timedelta_for_answers = datetime.timedelta(0, 30)
    last_round = 3

    def reset_game(self):
        self.round = 1
        self.status = "waiting"
        self.question = None
        self.guesses = {}
        self.answers = {}
        self.score_changes = {}
        self.time_to_switch = None
        for user_id in self.user_ids:
            user = User.load(user_id)
            user.score = 0
            user.save()

    def __init__(self):
        self.room_id = self.create_random_id()
        self.user_ids = []
        self.host = None
        self.reset_game();

    def set_guess(self, user_id, guess):
        if self.status == 'questionguess':
            self.guesses[user_id] = guess
            if len(self.user_ids) == len(self.guesses):
                self.advance_state(ignore_time=True)
        else:
            logging.info("User %s tried to guess %s when room state was %s" % (user_id, guess, self.status))

    def set_answer(self, user_id, answer):
        if self.status == 'questionanswer':
            if answer in self.guesses.values() or answer == self.question.answer or answer in self.question.get_just_answers():
                self.answers[user_id] = answer
                if len(self.user_ids) == len(self.answers):
                    self.advance_state(ignore_time=True)
            else:
                logging.warn("User %s tried to answer %s but it wasn't found in %s" % (user_id, answer, string.join(self.guesses.values(), ', ')))
        else:
            logging.info("User %s tried to answer %s when room state was %s" % (user_id, answer, self.status))

    def start_game(self):
        self.status = "round"
        self.round = 1
        self.time_to_switch = datetime.datetime.now() + Room.timedelta_for_information

    def upsert_user(self, user_id):
        if not user_id in self.user_ids:
            self.user_ids.append(user_id)

    def score_question(self):
        # Check the initial guesses
        for guess_user_id, guess in self.guesses.items():
            if guess == self.question.answer:
                # User guessed correctly
                self.score_changes[guess_user_id] = self.score_changes.get(guess_user_id, 0) + 500
                logging.info('+500 the user %s who guessed the answer %s initially' % (guess_user_id, guess))

        for answer_user_id, answer in self.answers.items():
            if answer == self.question.answer:
                # User picked correctly
                self.score_changes[answer_user_id] = self.score_changes.get(answer_user_id, 0) + 250
                logging.info('+250 for the user %s who picked the right answer %s' % (answer_user_id, answer))
            else:
                # User picked incorrectly, reward the sneaky player
                for sneaky_user_id, guess in self.guesses.items():
                    if answer == guess and sneaky_user_id != answer_user_id:
                        # Reward the user who made the guess
                        self.score_changes[sneaky_user_id] = self.score_changes.get(sneaky_user_id, 0) + 100
                        logging.info('+100 for the user %s who made the guess %s' % (sneaky_user_id, guess))

        for user_id, amount in self.score_changes.items():
            user = User.load(user_id)
            user.score += amount
            user.save()
            logging.info("%d total added to %s's score" % (amount, user.nickname))


    def pick_wrong_answers(self):
        # TODO: Factor in the shows, picks, and likes to get better wrong answers
        possible_answers = [answer.upper() for answer in self.question.get_just_answers()]
        random.shuffle(possible_answers)
        self.wrong_answers = set(possible_answers[:max(1, 4 - len(set(self.guesses.values())))])

    def ask_new_question(self):
        self.guesses = {}
        self.answers = {}
        self.score_changes = {}
        # TODO: Make sure we don't pick the same question as before
        self.question = DbQuestion.get_random()
        self.question.answer = wordfixer.standardize_guess(self.question.answer)

    def advance_state(self, ignore_time):
        if ignore_time or (self.time_to_switch and self.time_to_switch < datetime.datetime.now()):
            if self.status == "round":
                self.status = "questionguess"
                self.time_to_switch = datetime.datetime.now() + Room.timedelta_for_answers
                self.ask_new_question()
                self.save()
            elif self.status == "questionguess":
                self.status = "questionanswer"
                self.time_to_switch = datetime.datetime.now() + Room.timedelta_for_answers
                self.pick_wrong_answers()
                self.save()
            elif self.status == "questionanswer":
                self.status = "questionreveal"
                self.time_to_switch = datetime.datetime.now() + Room.timedelta_for_information
                self.save()
            elif self.status == "questionreveal":
                self.score_question()
                self.status = "questionscore"
                self.time_to_switch = datetime.datetime.now() + Room.timedelta_for_information
                self.save()
            elif self.status == "questionscore":
                self.status = "score"
                self.time_to_switch = datetime.datetime.now() + Room.timedelta_for_information
                self.save()
            elif self.status == "score":
                self.round = self.round + 1
                self.time_to_switch = datetime.datetime.now() + Room.timedelta_for_information
                if self.round > Room.last_round:
                    self.status = "gameover"
                else:
                    self.status = "round"
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
        # Fix hosts if it accidentally goes bad
        if not self.host in self.user_ids and len(self.user_ids) > 0:
            self.host = self.user_ids[0]
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

class SpellingSuggestionMessage(object):
    def __init__(self, suggestions):
        self.message_type = 'spellingsuggestion'
        self.suggestions = suggestions

class RoomStateMessage(object):
    def __init__(self, room, user):
        self.message_type = "room"
        self.room_id = room.room_id
        self.room = self.get_state(room, user.user_id)

    def get_state(self, room, user_id):
        switch_interval = (room.time_to_switch - datetime.datetime.now()).total_seconds() * 1000.0 if room.time_to_switch and room.host == user_id else None
        users = [User.load(user_id) for user_id in room.user_ids]

        if room.status == 'waiting':
            return dict(
                room_id = room.room_id,
                status = room.status,
                users = [dict(nickname=user.nickname, is_ready=user.is_ready) for user in users],
                )
        elif room.status == "round":
            return dict(
                room_id = room.room_id,
                status = room.status,
                round = room.round,
                is_last_round = room.round == Room.last_round,
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
            all_guesses = { guess for guess in room.guesses.values() }
            all_guesses.add(room.question.answer)
            all_guesses |= room.wrong_answers
            return dict(
                room_id = room.room_id,
                status = room.status,
                guesses = list(all_guesses),
                question = room.question.question,
                time_to_switch = room.time_to_switch,
                switch_interval = switch_interval
                )
        elif room.status == "questionreveal":
            all_guesses = { guess for guess in room.guesses.values() }
            all_guesses.add(room.question.answer.upper())
            all_guesses |= room.wrong_answers
            guessers_for_guesses = { guess:[] for guess in all_guesses }
            for user_id, guess in room.answers.items():
                guessers_for_guesses[guess].append([user.nickname for user in users if user.user_id == user_id][0])
            guesses = [dict(
                answer=guess,
                guessers=guessers_for_guesses[guess],
                is_correct=(guess == room.question.answer)
                ) for guess in all_guesses]
            return dict(
                room_id = room.room_id,
                status = room.status,
                guesses = guesses,
                question = room.question.question,
                time_to_switch = room.time_to_switch,
                switch_interval = switch_interval
                )
        elif room.status == "questionscore":
            return dict(
                room_id = room.room_id,
                status = room.status,
                users = [dict(
                    nickname=user.nickname,
                    score_change=room.score_changes.get(user.user_id, 0)
                    ) for user in users],
                question = room.question.question,
                time_to_switch = room.time_to_switch,
                switch_interval = switch_interval
                )
        elif room.status == "score":
            return dict(
                room_id = room.room_id,
                status = room.status,
                users = [dict(
                    nickname=user.nickname,
                    score=user.score,
                    score_change=room.score_changes.get(user.user_id, 0)
                    ) for user in users],
                time_to_switch = room.time_to_switch,
                switch_interval = switch_interval
                )
        elif room.status == "gameover":
            return dict(
                room_id = room.room_id,
                status = room.status,
                users = [dict(nickname=user.nickname, score=user.score) for user in users]
                )


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
            template_values = { "alert": "The room was not found", "alert_class":"danger"}
        if (self.request.get("reason") == "question_added"):
            template_values = { "alert": "The Question was succssesfuly added to the database!", "alert_class":"success"}
        if (self.request.get("reason") == "no_questions"):
            template_values = { "alert": "No more question to evaluate!", "alert_class":"info"}
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
            room.advance_state(ignore_time=False)
            self.add_room_message(room.room_id, RoomStateMessage(room, user))
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
        self.add_room_message(room.room_id, RoomStateMessage(room, user))
        self.send_messages()

class RoomSetNicknameHandler(BaseRoomHandler):
    def post(self, room_id):
        room_id = room_id.upper()
        (room, user) = self.get_room_and_user(room_id)
        newnickname = self.request.get('newnickname').upper().strip()
        logging.info("Renaming user %s to %s" % (user.nickname, newnickname))

        if not room:
            logging.warn("Room does not exist")
            return

        if newnickname == user.nickname or len(newnickname) == 0:
            logging.info("Did not change nickname")
            return

        # TODO: Remove potentially obscene room names

        user.nickname = newnickname
        user.save()
        self.add_user_message(user.user_id, NewNicknameMessage(user.nickname))
        self.add_room_message(room.room_id, RoomStateMessage(room, user))
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

class RoomRestartGameHandler(BaseRoomHandler):
    def post(self, room_id):
        room_id = room_id.upper()
        (room, user) = self.get_room_and_user(room_id)
        logging.info("Game restart requested for %s by %s" % (room_id, user.user_id))


        if not room:
            logging.warn("Room does not exist")
            return

        if room.status == "gameover":
            room.reset_game()
            room.save()

            self.add_room_message(room.room_id, RoomStateMessage(room, user))
            self.send_messages()

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

        self.add_room_message(room.room_id, RoomStateMessage(room, user))
        self.send_messages()

class RoomSendGuessHandler(BaseRoomHandler):
    def post(self, room_id):
        room_id = room_id.upper()
        (room, user) = self.get_room_and_user(room_id)
        guess = self.request.get('guess').upper()
        logging.info("Guess %s received %s by %s" % (guess, room_id, user.user_id))

        if not room:
            logging.warn("Room does not exist")
            return

        # Standardize any numeric answers
        guess = wordfixer.standardize_guess(guess)
        logging.info("Guess standardized: %s" % guess)

        room.set_guess(user.user_id, guess)
        room.save()

        # Check for spelling suggestions
        spelling = wordfixer.standardize_guess(wordfixer.correct(guess).upper())
        if spelling != guess:
            suggestions = [spelling]

            # Send message to let them update their guess
            self.add_user_message(user.user_id, SpellingSuggestionMessage(suggestions))

        self.add_room_message(room.room_id, RoomStateMessage(room, user))
        self.send_messages()

class RoomSendAnswerHandler(BaseRoomHandler):
    def post(self, room_id):
        room_id = room_id.upper()
        (room, user) = self.get_room_and_user(room_id)
        answer = self.request.get('answer').upper()
        logging.info("Answer %s received %s by %s" % (answer ,room_id, user.user_id))

        if not room:
            logging.warn("Room does not exist")
            return

        room.set_answer(user.user_id, answer)
        room.save()

        self.add_room_message(room.room_id, RoomStateMessage(room, user))
        self.send_messages()

class NewQuestionHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'newquestion.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        question = self.request.get("question")
        answer=self.request.get("answer")
        name=self.request.get("name")
        fakeanswers=[]
        fakeanswers.append(self.request.get("fakeanswer1"))
        fakeanswers.append(self.request.get("fakeanswer2"))
        fakeanswers.append(self.request.get("fakeanswer3"))
        if self.request.get("fakeanswer4"):
            fakeanswers.append(self.request.get("fakeanswer4"))
        if self.request.get("fakeanswer5"):
            fakeanswers.append(self.request.get("fakeanswer5"))

        DbNewQuestion(question=question, answer=answer, fakeanswers=fakeanswers).put()

        url = self.request.host_url + "?reason=question_added"
        return self.redirect(url)

# TODO: May want to add additonal answers as spelling suggestions
# TODO: Add back in the "answers to the questions" as potential spelling words [question.answer for question in questions]
wordfixer = WordFixer(os.path.join(os.path.split(__file__)[0], 'data/words.txt'))

app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/newquestion',NewQuestionHandler),

    ('/room/?', RoomCreateHandler),
    ('/room/([A-Za-z]+)', RoomViewHandler),
    ('/room/([A-Za-z]+)/checkstate', RoomCheckStateHandler),
    ('/room/([A-Za-z]+)/connect', RoomConnectHandler),
    ('/room/([A-Za-z]+)/restartgame', RoomStartGameHandler),
    ('/room/([A-Za-z]+)/sendguess', RoomSendGuessHandler),
    ('/room/([A-Za-z]+)/sendanswer', RoomSendAnswerHandler),
    ('/room/([A-Za-z]+)/setnickname', RoomSetNicknameHandler),
    ('/room/([A-Za-z]+)/startgame', RoomStartGameHandler)
    ], debug=True)
