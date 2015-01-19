from google.appengine.ext import db

class DbNewQuestion(db.Model):
    question = db.StringProperty(required=True, indexed=False)
    answer = db.StringProperty(required=True, indexed=False)
    fakeanswers = db.StringListProperty(indexed=False)
    created = db.DateTimeProperty(auto_now_add=True)
