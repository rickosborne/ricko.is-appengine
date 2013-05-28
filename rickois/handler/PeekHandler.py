#!/usr/bin/env python

from TemplatedHandler import TemplatedHandler
from django.utils import simplejson
from rickois.model.GoLinkModel import peek_golink
import yaml
import logging
from google.appengine.ext import db

class PeekHandler(TemplatedHandler):
    _ignored_props = { 'ownerid': True, 'gohits': True }
    
    def get(self):
        link = self.path_link()
        ext = self.ext()
        if (ext == '') or (not ext): ext = '.html'
        template = 'peek' + ext
        scope = {'data': ''}
        if not link:
            scope['status_code'] = 404
            scope['status_txt'] = 'NOT_FOUND'
            if (ext == '.js') or (ext == '.json') or (ext == '.yaml'):
                scope['data'] = 'null'
        else:
            scope['status_code'] = 200
            scope['status_txt'] = 'OK'
            link = peek_golink(link.name, self.ip(), self.referer(), self.ua())
            data = {}
            for prop in (a for a in dir(link) if not a.startswith('_')):
                value = getattr(link, prop)
                if callable(value) or prop in self._ignored_props:
                    continue
                elif (not isinstance(value, (str,int,float,long,unicode,bool,type(None)))) or (ext == '.yaml'):
                    data[prop] = str(value)
                else:
                    data[prop] = value
            scope['data'] = data
            if (ext == '.js') or (ext == '.json'):
                scope['status_code'] = simplejson.dumps(obj=scope['status_code'], skipkeys=True)
                scope['status_txt'] = simplejson.dumps(obj=scope['status_txt'], skipkeys=True)
                scope['data'] = simplejson.dumps(obj=scope['data'], skipkeys=True)
                scope['callback'] = self.query_var('callback')
            elif ext == '.yaml':
                scope['data'] = yaml.dump({'data': data}, default_flow_style=False).replace("data:", '', 1)
            else:
                scope['link'] = link 
        self.render(template, scope)
