# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import urllib
import re
import cPickle
import sys
import tweepy
from twToken import *

def getTwitterAccounts(event_id):
    snames = parseEventPage(event_id)
    return snames

def parseUserPage(url):
    print url
    response = urllib.urlopen(url)
    source = response.read()

    soup = BeautifulSoup(source)
    social = soup.find('p', {'class': 'social_link clearfix'})
    twitter = social.find('img', alt='Twitter')
    if twitter:
        return re.sub(re.compile(ur".*/"), "", twitter.parent['href'])
    else:
        return None
   
def parseEventPage(event_id):
    url = "http://connpass.com/event/%s/" % event_id
    response = urllib.urlopen(url)
    source = response.read()

    soup = BeautifulSoup(source)
    ownerArea = soup.find('ul', {'class': 'owner_list clearfix'})
    owners = ownerArea.findAll('li')
    names = set(['http://connpass.com' + owner.find('a')['href']
                 for owner in owners])

    sideArea = soup.find('div', {'class': 'side_sec_box side_article_area'})
    users = sideArea.findAll('p', {'class': 'user'})
    names = names | set(['http://connpass.com' + user.a['href']
                         for user in users])

    snames = []
    for name in names:
        sname = parseUserPage(name)
        if sname:
            snames.append(sname)
    return snames
