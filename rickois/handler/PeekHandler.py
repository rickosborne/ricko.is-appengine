#!/usr/bin/env python

from TemplatedHandler import TemplatedHandler
from rickois.model.GoLinkModel import peek_golink

class PeekHandler(TemplatedHandler):
    def get(self):
        link = self.path_link()
        if not link:
            self.render('missing.html')
            return
        peek_golink(link.name, self.ip(), self.referer(), self.ua())
        self.render('peek.html', {'link': link})

