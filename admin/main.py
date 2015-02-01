import datetime
import logging
import json
import os
import random
import time
import string
import uuid
import webapp2
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models.dbquestion import DbQuestion, DbAnswer, import_questions_if_needed, export_questions, delete_all_questions
from models.dbnewquestion import DbNewQuestion

class AdminIndexHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
class AdminNewAnswerHandler(webapp2.RequestHandler):
    def get(self):
        try:
            offset = int(self.request.get('offset'))
        except ValueError:
            offset = 0
        query = DbQuestion.all()
        questions = list(query.run(limit=1, offset=offset))

        if not questions:
            url = self.request.host_url + "?reason=no_questions"
            return self.redirect(url)
        question = questions[0]
        fakeanswers = question.answers
        template_values = {
            "question": question.question,
            "answer": question.answer,
            "fakeanswers": fakeanswers
            }
        path = os.path.join(os.path.dirname(__file__), 'newanswer.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        try:
            offset = int(self.request.get('offset'))
        except ValueError:
            offset = 0
        if self.request.get('approve'):
            query = DbNewQuestion.all()
            questions = list(query.run(limit=1, offset=offset))
            newquestion = questions[offset]
            question = DbQuestion(
                index=DbQuestion.get_highest_index() + 1,
                question=self.request.get('question'),
                answer=self.request.get('answer'),
                theme="Miscellaneous")
            for fakeanswer in self.request.get_all('fakeanswers'):
                DbAnswer(question=question, text=fakeanswer).put()
            question.put()
            newquestion.delete()
            url = self.request.path_url + "?offset=" + str(offset)
            return self.redirect(url)
        elif self.request.get('skip'):
            url = self.request.path_url + "?offset=" + str(offset+1)
            return self.redirect(url)
        elif self.request.get('delete'):
            query=DbNewQuestion.all()
            questions = list(query.run(limit=1, offset=offset))
            questions[offset].delete()
            url = self.request.path_url + "?offset=" + str(offset)
            return self.redirect(url)
        else:
            logging.warn("Failed to post!")


class AdminNewQuestionHandler(webapp2.RequestHandler):
    def get(self):
        try:
            offset = int(self.request.get('offset'))
        except ValueError:
            offset = 0
        query = DbNewQuestion.all()
        questions = list(query.run(limit=1, offset=offset))

        if not questions:
            url = self.request.host_url + "?reason=no_questions"
            return self.redirect(url)
        question = questions[0]
        fakeanswers = question.fakeanswers
        fakeanswers.append("")
        template_values = {
            "question": question.question,
            "answer": question.answer,
            "fakeanswers": fakeanswers
            }
        path = os.path.join(os.path.dirname(__file__), 'newquestion.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        try:
            offset = int(self.request.get('offset'))
        except ValueError:
            offset = 0
        if self.request.get('approve'):
            query = DbNewQuestion.all()
            questions = list(query.run(limit=1, offset=offset))
            newquestion = questions[offset]
            question = DbQuestion(
                index=DbQuestion.get_highest_index() + 1,
                question=self.request.get('question'),
                answer=self.request.get('answer'),
                theme="Miscellaneous")
            for fakeanswer in self.request.get_all('fakeanswers'):
                DbAnswer(question=question, text=fakeanswer).put()
            question.put()
            newquestion.delete()
            url = self.request.path_url + "?offset=" + str(offset)
            return self.redirect(url)
        elif self.request.get('skip'):
            url = self.request.path_url + "?offset=" + str(offset+1)
            return self.redirect(url)
        elif self.request.get('delete'):
            query=DbNewQuestion.all()
            questions = list(query.run(limit=1, offset=offset))
            questions[offset].delete()
            url = self.request.path_url + "?offset=" + str(offset)
            return self.redirect(url)
        else:
            logging.warn("Failed to post!")

class AdminExportHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("<pre>\n")
        for line in export_questions():
            self.response.out.write("%s\n" % line)
        self.response.out.write("</pre>\n")

class AdminImportHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Importing')
        delete_all_questions()
        import_questions_if_needed()
        self.response.out.write(' complete')

app = webapp2.WSGIApplication([
    ('/admin',AdminIndexHandler),
    ('/admin/newanswer',AdminNewAnswerHandler),
    ('/admin/newquestion', AdminNewQuestionHandler),
    ('/admin/questions/export', AdminExportHandler),
    ('/admin/questions/import', AdminImportHandler)
    ], debug=True)
