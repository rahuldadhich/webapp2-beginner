import cgi
import datetime
import webapp2
import logging
import os

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext.webapp import template


class Superuser(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    username = ndb.TextProperty()
    password = ndb.TextProperty()


class LoginPage(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'template/login.html')
        self.response.out.write(template.render(path, template_values))


class SignPost(webapp2.RequestHandler):
    def post(self):
        user = Superuser(username=self.request.get('username'),password=self.request.get('password'))
        # self.response.out.write(user.put().urlsafe())
        user.put()
        self.redirect('/home')

class MainPage(webapp2.RequestHandler):
    def get(self):
        qry_result = Superuser.query().fetch()
        # self.response.out.write(qry_result)
        template_values = {
            'users': qry_result
        }
        path = os.path.join(os.path.dirname(__file__), 'template/dashboard.html')
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([
  ('/', LoginPage),
  ('/sign', SignPost),
  ('/home', MainPage),
], debug=True)
