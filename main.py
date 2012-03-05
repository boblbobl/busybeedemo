import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from google.appengine.ext.webapp import template

from models import *

class MainHandler(webapp.RequestHandler):
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
    
    template_values = {
      'action': action,
      'pages': pages
    }

    if page_name:
      if page_name == 'signup':
        template_page = os.path.join(os.path.dirname(__file__), 'templates/signup.html')
      elif page_name == 'sitemap':
        template_page = os.path.join(os.path.dirname(__file__), 'templates/sitemap.html')
      elif page_name == 'terms':
        template_page = os.path.join(os.path.dirname(__file__), 'templates/terms.html')
      elif Page.page_exist(page_name):
        p = pages.filter('name = ', page_name).get()
        
        page_values = {
          'title': p.title,
          'meta_description': '' if p.meta_description == None else p.meta_description,
          'meta_keywords': '' if p.meta_keywords == None else p.meta_keywords
        }
        template_values.update(page_values)
        template_page = os.path.join(os.path.dirname(__file__), 'templates/empty.html')
      else:
        template_page = os.path.join(os.path.dirname(__file__), 'templates/404.html')
    else:
      template_page = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    
    self.response.out.write(template.render(template_page, template_values))


def main():
  application = webapp.WSGIApplication([('/.*', MainHandler)], debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
