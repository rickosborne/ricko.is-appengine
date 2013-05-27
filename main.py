#!/usr/bin/env python

from google.appengine.api import users
from rickois.handler.LoginHandler import LoginHandler
from rickois.handler.LogoutHandler import LogoutHandler
from rickois.handler.NewLinkHandler import NewLinkHandler
from rickois.handler.TemplatedHandler import TemplatedHandler
from rickois.model import GoLinkModel
import webapp2

class MainHandler(TemplatedHandler):
    def get(self):
        user = users.get_current_user()
        do_logging = not( users.is_current_user_admin() )
        path = self.request.path
        if path[:1] == '/': # trim leading slash
            path = path[1:]
        link = GoLinkModel.get_golink(path)
        # self.response.write('Hello world: %s\n' % path)
        # self.response.write('Link: %s' % link)
        self.render('index.html')

    def post(self):
        self.response.headers['Content-Type'] = 'text/plain'

app = webapp2.WSGIApplication([
    ('/_/login', LoginHandler),
    ('/_/logout', LogoutHandler),
    ('/_/new', NewLinkHandler),
    ('.*', MainHandler)
], debug=True)

