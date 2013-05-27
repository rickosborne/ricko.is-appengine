#!/usr/bin/env python

from TemplatedHandler import TemplatedHandler

class PeekHandler(TemplatedHandler):
    def get(self):
        link = self.path_link()
        self.render('peek.html', {'link': link})

