#!/usr/bin/env python

from google.appengine.api import users
from rickois.handler.LoginHandler import LoginHandler
from rickois.handler.LogoutHandler import LogoutHandler
from rickois.handler.NewLinkHandler import NewLinkHandler
from rickois.handler.TemplatedHandler import TemplatedHandler
from rickois.handler.PeekHandler import PeekHandler
from rickois.model.GoLinkModel import hit_golink
import webapp2

class MainHandler(TemplatedHandler):
    def get(self):
        do_logging = not( users.is_current_user_admin() )
        link = self.path_link()
        if not link:
            if len(self.path()):
                self.render('missing.html')
            else:
                self.render('index.html')
            return
        hit_golink(link.name)
        self.response.write('Link: %s' % link.href)

app = webapp2.WSGIApplication([
    ('/_/login', LoginHandler),
    ('/_/logout', LogoutHandler),
    ('/_/new', NewLinkHandler),
    ('.*\\+', PeekHandler),
    ('.*', MainHandler)
], debug=True)

