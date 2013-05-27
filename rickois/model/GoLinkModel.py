#!/usr/bin/env python

from google.appengine.ext import db
from google.appengine.api import users

class GoLink(db.Model):
    name = db.StringProperty(verbose_name='Unique short identifier', multiline=False, required=True, indexed=True)
    created = db.DateTimeProperty(verbose_name='When the link was created', auto_now=False, auto_now_add=True, required=True, indexed=True)
    updated = db.DateTimeProperty(verbose_name='When the link was last updated', auto_now=True, auto_now_add=True, required=True, indexed=True)
    ownerid = db.StringProperty(verbose_name='Creator of the link', required=True, indexed=True)
    hits = db.IntegerProperty(verbose_name='Total click-throughs', default=0, required=True)
    peeks = db.IntegerProperty(verbose_name='Total requests for metadata', default=0, required=True)
    href = db.LinkProperty(verbose_name='Destination address', required=True)
    title = db.StringProperty(verbose_name='Human-readable title of the destination', required=True)
    
@db.transactional
def hit_golink(name):
    if users.is_current_user_admin(): return
    link = get_golink(name)
    link.hits += 1
    link.put()

@db.transactional
def peek_golink(name):
    if users.is_current_user_admin(): return
    link = get_golink(name)
    link.peeks += 1
    link.put()

def get_golink(name=None):
    if not name:
        return None
    key = db.Key.from_path('GoLink', name)
    link = db.get(key)
    return link

@db.transactional
def new_golink(name, href, title):
    link = get_golink(name)
    if link:
        return None
    link = GoLink(key_name=name, name=name, href=href, title=title, ownerid=users.get_current_user().user_id(), hits=0, peeks=0)
    db.Model.put(link)
    return link