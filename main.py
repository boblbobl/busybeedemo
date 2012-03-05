import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from google.appengine.ext.webapp import template
from google.appengine.api import memcache

import urllib2
from google.appengine.api import urlfetch

from django.utils import simplejson

from models import *

class MainHandler(webapp.RequestHandler):
  def get_tweets(self):
    tweets = memcache.get("tweets")
    if tweets is not None:
      return tweets
    else:
      twitter = urllib2.urlopen('https://api.twitter.com/1/statuses/user_timeline.json?screen_name=busybeemanager&count=3')
      twitter_json = twitter.read()
    
      data = simplejson.loads(twitter_json)
      memcache.add("tweets", data, 3600)
      return data
  
  def get_pages(self):
    pages = Page.all().order("name")
    return pages
  
  def get_page_name(self, path):
    pagename = ''
    if len(path) > 1:
      pagename = path[1].lower()
    return pagename

  def get_variable(self, path, i):
    pathCount = 2 + i
    variable = None
    if len(path) > pathCount:
      variable = path[pathCount].lower()
    return variable
  
  def get_action(self, path):
    action = None
    if len(path) > 2:
      action = path[2].lower()
    return action
  
  def get(self):
    path = self.request.path.split('/')
    page_name = self.get_page_name(path)
    action = self.get_action(path)
    
    pages = self.get_pages()
    tweets = self.get_tweets()
    
    template_values = {
      'name': page_name,
      'action': action,
      'pages': pages,
      'tweets': tweets
    }

    if page_name:
      if page_name == 'signup' and action is None:
        template_page = os.path.join(os.path.dirname(__file__), 'templates/signup.html')
      elif page_name == 'sitemap' and action is None:
        template_page = os.path.join(os.path.dirname(__file__), 'templates/sitemap.html')
      elif page_name == 'terms' and action is None:
        template_page = os.path.join(os.path.dirname(__file__), 'templates/terms.html')
      elif Page.page_exist(page_name):
        p = pages.filter('name = ', page_name).get()
        
        page_values = {
          'title': p.title,
          'meta_description': '' if p.meta_description == None else p.meta_description,
          'meta_keywords': '' if p.meta_keywords == None else p.meta_keywords,
          'content': '' if p.content == None else p.content,
          'edit': True if action == 'edit' else False
        }
        template_values.update(page_values)
        template_page = os.path.join(os.path.dirname(__file__), 'templates/page.html')
      else:
        #TODO: Handle legacy site urls
        template_page = os.path.join(os.path.dirname(__file__), 'templates/404.html')
        self.error(404)
    else:
      template_page = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    
    self.response.out.write(template.render(template_page, template_values))


def main():
  application = webapp.WSGIApplication([('/.*', MainHandler)], debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
