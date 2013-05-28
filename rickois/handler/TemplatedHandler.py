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
    extensions = {
        '.json': 'application/json',
        '.js'  : 'text/javascript',
        '.xml' : 'text/xml',
        '.yaml': 'text/plain'
    }
    _path = None
    _ext = None
    _peek = None
    _content_type = None
    
    def extract_path(self):
        path = self.request.path
        if path[:1] == '/': # trim leading slash
            path = path[1:]
        if path[-1:] == '+': # trim trailing +
            path = path[:-1]
            self._peek = True
        else:
            self._peek = False
        self._ext = ''
        self._content_type = 'text/html'
        for ext, content_type in self.extensions.iteritems():
            if path[-len(ext):].lower() == ext:
                self._ext = ext
                self._content_type = content_type
                path = path[:-len(ext)]
                break
        self._path = path
    
    def content_type(self):
        if self._content_type is None:
            self.extract_path()
        return self._content_type
    
    def ext(self):
        if self._ext is None:
            self.extract_path()
        return self._ext
    
    def is_peek(self):
        if self._ext is None:
            self.extract_path()
        return self._peek
    
    def path(self):
        if self._path is None:
            self.extract_path()
        return self._path
    
    def ip(self):
        return self.request.remote_addr
    
    def ua(self):
        return self.request.headers.get('User-Agent', None)
    
    def referer(self):
        return self.request.headers.get('Referer', None)
    
    def path_link(self):
        return get_golink(self.path())
    
    def query_var(self, name):
        if name in self.request.GET:
            return self.request.GET[name]
        return None
    
    def render(self, name, values={}):
        template = JINJA_ENVIRONMENT.get_template(name)
        self.response.headers['Content-Type'] = self.content_type()
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