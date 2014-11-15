#!/usr/bin/env python

import requests
import json
import sys
from os.path import realpath, join, dirname
from urllib.parse import urljoin
from termcolor import colored

def main():
    settings = None
    data     = None
    settings_file = join(dirname(realpath(__file__)), "settings.json")
    query = " ".join(sys.argv[1:])

    with open(settings_file, "r") as f:
        settings = json.loads(f.read())

    # FIXME: non-static timestamp
    url=construct_url(settings, '1414800000')
    http_auth = requests.auth.HTTPBasicAuth(settings['username'], settings['password'])
    r = requests.get(url, auth=http_auth)
    data = r.json()
    #r = requests.post("http://api.trakt.tv/account/test/" + api_key, data=json.dumps(auth))

    #with open('feed.json', 'r') as f:
        #data = json.loads(f.read())


    title = lambda j: j['show']['title']
    # FIXME: Multiple episodes
    sea   = lambda j: j['episodes'][0]['season']
    ep    = lambda j: j['episodes'][0]['episode']
    time  = lambda j: j['timestamp']
    seen = sorted([(title(j), sea(j), ep(j), time(j))
                   for j in data['activity'] if query in title(j).lower()], key=lambda k: k[3])


    for s in seen:
        title = colored(s[0], 'cyan')
        season = colored(str(s[1]), 'blue')
        episode = colored(str(s[2]), 'green')
        print(title + ' (' + season + 'x'+ episode + ')')

def construct_url(settings, start_ts='/'):
    parts=[settings['api'], settings['username'], 'episode', 'seen', start_ts]
    url='http://api.trakt.tv/activity/user.json/'
    for p in parts:
        url = urljoin(url, p + '/');
    return url[:-1] + "?min=1"

if __name__ == '__main__':
    main()
