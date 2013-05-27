#!/usr/bin/env python

from google.appengine.ext import db
from google.appengine.api import memcache
import re

class AgentRuleMatch():
    vendor = None
    major = None
    ver = None
    mobile = None
    bot = None

class AgentRule(db.Model):
    priority = db.IntegerProperty(verbose_name='Sequence in which the rule will apply', required=True, indexed=True)
    regex = db.StringProperty(verbose_name='Regular expression to extract parts', required=True, indexed=False)
    vendor = db.StringProperty(verbose_name='The vendor extracted from the UA', required=True, indexed=True)
    majoridx = db.IntegerProperty(verbose_name='Index of the major version number', required=False, indexed=False)
    veridx = db.IntegerProperty(verbose_name='Index of the full version number', required=False, indexed=False)
    mobile = db.BooleanProperty(verbose_name='Is a mobile device?', required=False, indexed=True)
    bot = db.BooleanProperty(verbose_name='Is a robot?', required=False, indexed=True)
    _regex = None

    def apply_to(self, ua):
        if not self._regex:
            self._regex = re.compile(self.regex, re.UNICODE | re.IGNORECASE)
        result = self._regex.search(ua)
        if not result:
            return None
        match = AgentRuleMatch()
        if self.vendor: match.vendor = result.expand(self.vendor)
        if self.majoridx: match.major = result.group(self.majoridx)
        if self.veridx: match.ver = result.group(self.veridx)
        if self.mobile: match.mobile = self.mobile
        if self.bot: match.bot = self.bot
        return match

def get_rules():
    rules = memcache.Client().get('agent_rules')
    if not rules:
        rules = []
        for rule in AgentRule.all().order('priority').run():
            rules.append(rule)
        memcache.Client().add('agent_rules', rules, 60)
    return rules

def match_agent(ua):
    rules = get_rules()
    for rule in rules:
        match = rule.apply_to(ua)
        if match:
            return match
    return None
