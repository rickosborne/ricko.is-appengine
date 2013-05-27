#!/usr/bin/env python

import os
import webapp2
import jinja2

TEMPLATE_PATH = '_templates'
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), TEMPLATE_PATH)), extensions=['jinja2.ext.autoescape'])

class TemplatedHandler(webapp2.RequestHandler):
    
    def render(self, name, values={}):
        template = JINJA_ENVIRONMENT.get_template(name)
        self.response.write(template.render(values))
