#!/usr/bin/env python

'''
@author: rosborne
'''
from google.appengine.api import users

import webapp2

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect(users.create_login_url('/'))

