# -*- coding: utf-8 -*-

import sys, os
import cPickle
import json
import urllib

import tweepy
from twToken import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

nodesFile = sys.argv[1]
nodes = cPickle.load(open(nodesFile))

site, event_id = nodesFile.split('.')[0].split('_')[:2]
vfname = '%s_%s_visited.pkl' % (site, event_id)
efname = '%s_%s_edges.pkl' % (site, event_id)

# 訪問済みnodeはvisitedに格納
if not os.path.exists(vfname):
    visited = []
else:
    visited = cPickle.load(open(vfname))

# edgesはedgesに保存
if not os.path.exists(efname):
    edges = {}
else:
    edges = cPickle.load(open(efname))

# 未訪問nodesのみ取り出す
sources = list(set(nodes.keys()) - set(visited))

try:
    for i, source in enumerate(sources):
        print i+1, len(sources), source
        dests = api.friends_ids(user_id=source)
        edges[source] = dests
        visited.append(source)
    print '取得完了しました。'
except Exception, E:
    print E
    print 'API切れの可能性があります。'
    print 'しばらく待ってから再実行してください。'
finally:
    # 異常終了時もedgesとvisitedは永続化
    cPickle.dump(visited, open(vfname, 'w'))
    cPickle.dump(edges, open(efname, 'w'))
