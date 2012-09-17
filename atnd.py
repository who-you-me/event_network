# -*- coding: utf-8 -*-

import sys
import urllib
import json
import cPickle as pickle
import tweepy
from twToken import *

def getTwitterAccounts(event_id):
    snames = events_users(event_id)
    return snames

def events_users(event_id):
    ep = 'http://api.atnd.org/events/users/?'
    params = {'event_id': event_id, 'format': 'json'}

    url = ep + urllib.urlencode(params)
    response = urllib.urlopen(url)
    source = json.loads(response.read())

    snames = set([user['twitter_id'] for event in source['events']
                  for user in event['users'] if user['twitter_id']])
    return list(snames)
