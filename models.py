from google.appengine.ext import db

class Subscriber(db.Model):
  email = db.StringProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True)
  
  def email_exist(email):
    if Subscriber.all().filter('email =', email).get():
      return True
    else:
      return False
  email_exist = staticmethod(email_exist)
  
  
class Page(db.Model):
  title = db.StringProperty(required=True)
  name = db.StringProperty(required=True)
  meta_description = db.StringProperty()
  meta_keywords = db.StringProperty()
  content = db.TextProperty()
  last_updated = db.DateTimeProperty(auto_now=True)
  created = db.DateTimeProperty(auto_now_add=True)

  def page_exist(name):
    if Page.all().filter('name =', name).get():
      return True
    else:
      return False
  page_exist = staticmethod(page_exist)