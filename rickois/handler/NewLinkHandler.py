#!/usr/bin/env python

from TemplatedHandler import TemplatedHandler
from rickois.model.GoLinkModel import get_golink, new_golink

class NewLinkHandler(TemplatedHandler):
    def get(self):
        self.require_auth()
        self.render('new.html')

    def post(self):
        self.require_auth()
        posts = self.post_vars({
                'name': '^[^\s/]+$',
                'href': '^[^\s]+$',
                'title': '^.+$'
            }, 'new.html')
        if not posts: return
        name = posts['name']
        href = posts['href']
        title = posts['title']
        link = get_golink(name)
        if link:
            posts['error'] = 'That name is taken.'
            self.render('new.html', posts)
            return
        link = new_golink(name, href, title)
        self.redirect('/' + name + '+')
#         self.response.headers['Content-Type'] = 'text/plain'
#         self.response.write('name: %s\n' % name)
#         self.response.write('href: %s\n' % href)
#         self.response.write('title: %s\n' % title)
