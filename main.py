#!/usr/bin/env python

from google.appengine.api import users
from rickois.handler.LoginHandler import LoginHandler
from rickois.handler.LogoutHandler import LogoutHandler
from rickois.handler.NewLinkHandler import NewLinkHandler
from rickois.handler.TemplatedHandler import TemplatedHandler
from rickois.handler.PeekHandler import PeekHandler
import webapp2

class MainHandler(TemplatedHandler):
    def get(self):
        do_logging = not( users.is_current_user_admin() )
        link = self.path_link()
        if link:
            self.response.write('Link: %s' % link.href)
            return
        self.render('index.html')

    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'

app = webapp2.WSGIApplication([
    ('/_/login', LoginHandler),
    ('/_/logout', LogoutHandler),
    ('/_/new', NewLinkHandler),
    ('.*\\+', PeekHandler),
    ('.*', MainHandler)
], debug=True)

