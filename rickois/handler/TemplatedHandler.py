#!/usr/bin/env python

from google.appengine.api import users
import os
import webapp2
import jinja2
import re
from rickois.model.GoLinkModel import get_golink 

TEMPLATE_PATH = '../../_templates'
JINJA_ENVIRONMENT = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), TEMPLATE_PATH)), extensions=['jinja2.ext.autoescape'])

class TemplatedHandler(webapp2.RequestHandler):
    
    def path_ispeek(self):
        return (self.request.path[-1:] == '+')
    
    def path(self):
        path = self.request.path
        if path[:1] == '/': # trim leading slash
            path = path[1:]
        if path[-1:] == '+': # trim trailing +
            path = path[:-1]
        return path
    
    def ip(self):
        return self.request.remote_addr
    
    def ua(self):
        return self.request.headers.get('User-Agent', None)
    
    def referer(self):
        return self.request.headers.get('Referer', None)
    
    def path_link(self):
        return get_golink(self.path())
    
    def render(self, name, values={}):
        template = JINJA_ENVIRONMENT.get_template(name)
        self.response.write(template.render(values))

    def require_auth(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.path))
        return user

    def post_vars(self, names={}, template='error.html', block='error', values={}):
        missing = []
        present = {}
        for name, exp in names.iteritems():
            if name in self.request.POST:
                value = self.request.POST[name]
                if re.match(exp, value):
                    present[name] = value
                else:
                    missing.append(name)
            else:
                missing.append(name)
        if len(missing):
            values[block] = 'Missing: ' + ', '.join(missing)
            for name in missing:
                values[name] = ''
            for name, value in present.iteritems():
                values[name] = value
            self.render(template, values)
            return None
        return present