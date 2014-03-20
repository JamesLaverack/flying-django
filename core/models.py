from google.appengine.ext import db

class Comment(db.Model):
    author = db.StringProperty(required=True)
    content = db.StringProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)

class BlogPost(db.Model):
    author = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    content = db.StringProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    comments = db.ReferenceProperty(Comment)

