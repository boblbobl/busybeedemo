import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from google.appengine.ext.webapp import template


class MainHandler(webapp.RequestHandler):
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

    if page_name.lower() == 'signup':
      template_page = os.path.join(os.path.dirname(__file__), 'templates/signup.html')
    else:
      template_page = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    
    template_values = {
      'action': action
    }
    self.response.out.write(template.render(template_page, template_values))


def main():
  application = webapp.WSGIApplication([('/.*', MainHandler)], debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
