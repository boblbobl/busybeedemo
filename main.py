import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from google.appengine.ext.webapp import template


class MainHandler(webapp.RequestHandler):
  def get(self):
    template_page = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    template_values = {
    }
    self.response.out.write(template.render(template_page, template_values))


def main():
  application = webapp.WSGIApplication([('/', MainHandler)], debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()