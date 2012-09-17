# -*- coding: utf-8 -*-

import sys
import cPickle
import tweepy
import connpass
import atnd
from twToken import *

site = sys.argv[1]
event_id = sys.argv[2]

if site == 'connpass':
    snames = connpass.getTwitterAccounts(event_id)
elif site == 'atnd':
    snames = atnd.getTwitterAccounts(event_id)
else:
    # エラー発生させよう
    pass

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

users = {}
while snames:
    for user in api.lookup_users(screen_names=snames[:100]):
        if not user.protected:
            users[user.id] = user.screen_name
    snames = snames[100:]

fname = '%s_%s_nodes.pkl' % (site, event_id)
cPickle.dump(users, open(fname, 'w'))
