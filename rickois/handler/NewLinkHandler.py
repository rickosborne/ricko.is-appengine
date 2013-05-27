#!/usr/bin/env python

from google.appengine.api import users
from TemplatedHandler import TemplatedHandler

class NewLinkHandler(TemplatedHandler):
    def get(self):
        self.render('new.html')
