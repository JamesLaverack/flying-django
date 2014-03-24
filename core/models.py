from google.appengine.ext import db

class ContentItem(db.Model):
    author = db.StringProperty(required=True)
    author_name = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)    

class BlogPost(ContentItem):
    title = db.StringProperty(required=True)

class Comment(ContentItem):
    blogpost = db.ReferenceProperty(BlogPost, collection_name = "comments")
