#!/usr/bin/env python

from google.appengine.ext import db
from google.appengine.api import users
from AgentRuleModel import match_agent

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
def hit_golink_update(name, ip, referer=None, ua=None):
    if users.get_current_user(): return
    link = get_golink(name)
    link.hits += 1
    link.put()
    return link

def hit_golink(name, ip, referer=None, ua=None):
    if users.get_current_user(): return
    link = hit_golink_update(name, ip, referer, ua)
    new_gohit(link, ip, referer, ua, False)
    return link

@db.transactional
def peek_golink_update(name, ip, referer=None, ua=None):
    if users.get_current_user(): return
    link = get_golink(name)
    link.peeks += 1
    link.put()
    return link

def peek_golink(name, ip, referer=None, ua=None):
    if users.get_current_user(): return
    link = peek_golink_update(name, ip, referer, ua)
    new_gohit(link, ip, referer, ua, True)
    return link

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
    link = GoLink(key=db.Key.from_path('GoLink', name), name=name, href=href, title=title, ownerid=users.get_current_user().user_id(), hits=0, peeks=0)
    db.Model.put(link)
    return link

class GoHit(db.Model):
    link = db.ReferenceProperty(reference_class=GoLink, verbose_name='Source link', collection_name='gohits', required=True, indexed=True)
    created = db.DateTimeProperty(verbose_name='When the hit was created', auto_now=False, auto_now_add=True, required=True, indexed=True)
    ip = db.StringProperty(verbose_name='Remote IP address', multiline=False, required=True, indexed=True)
    referer = db.StringProperty(verbose_name='HTTP Referer (optional)', multiline=False, required=False, indexed=False)
    ua = db.StringProperty(verbose_name='User Agent (optional)', multiline=False, required=False, indexed=False)
    uavendor = db.StringProperty(verbose_name='User Agent vendor (optional)', multiline=False, required=False, indexed=True)
    uamajor = db.IntegerProperty(verbose_name='User Agent major version (optional)', required=False, indexed=True)
    uaver = db.FloatProperty(verbose_name='User Agent major version (optional)', required=False, indexed=True)
    mobile = db.BooleanProperty(verbose_name='Is a mobile device?', required=False, indexed=True)
    bot = db.BooleanProperty(verbose_name='Is a robot?', required=False, indexed=True)
    peek = db.BooleanProperty(verbose_name='Is a peek?', required=False, indexed=True, default=False)
    
    def put(self):
        db.Model.put(self)

def new_gohit(link, ip, referer, ua, peek=None):
    hit = GoHit(link=link, ip=ip, referer=referer, ua=ua)
    if ua is not None:
        match = match_agent(ua)
        if match:
            if match.vendor is not None: hit.vendor = match.vendor
            if match.major is not None: hit.major = match.major
            if match.ver is not None: hit.ver = match.ver
            if match.mobile is not None: hit.mobile = match.mobile
            if match.bot is not None: hit.bot = match.bot
    if peek is not None:
        hit.peek = peek
    hit.put()
