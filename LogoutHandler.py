#!/usr/bin/env python

'''
Created on May 26, 2013

@author: rosborne
'''
from google.appengine.api import users

import webapp2

class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect(users.create_logout_url('/'))

