#!/usr/bin/env python

from google.appengine.api import users
import webapp2

class NewLinkHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('New')

