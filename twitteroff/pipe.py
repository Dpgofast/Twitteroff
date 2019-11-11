'''
Second version Gh user breakdown pipeline
Take in username as sys.argv[1] and return jsons
built for use with node.js
'''

from dateutil import parser 
import json 
from requests import get as Get
import sys 

# t = 'token a3891'
# o = 'ba472'
# k = '73550e22'
# e = 'f22e5b6e'
# n = '1a478e14a63696'
# token  = t+o+k+e+n
# headers = {"Authorization":token}
# H = headers
base_url = 'https://api.github.com/users/'
com_url = 'https://api.github.com/repos/{}/commits?author={}'
simple = '?simple=yes&per_page=100&page=1'

def  grabber(username):
    '''
    Grab username return user stats json
    '''
    u = Get('https://api.github.com/users/{}?client_id={}&client_secret={}'.format(user, credentials.creds['CLIENT_ID'], credentials.creds['CLIENT_SECRET']))
    if u.ok:
        return u.json()
    else: 
        raise Exception('User not found')


def stats(username):
    '''
    Grab user data stats
    '''
    stuff = {}
    stuff['languages'] = {}
    stuff['repos'] = []
    ulink = grabber(username)
    reaper = ulink['repos_url'] + simple + '?client_id={}&client_secret={}      '.format(credentials.creds['CLIENT_ID'], credentials.creds['CLIENT_SECRET'])
    stats = Get(reaper)
    all_stat = stats.json()
    while 'next' in stats.links.keys():
        stats = Get(stats.links['next']['url']+'?client_id={}&client_secret={}'.format(credentials.creds['CLIENT_ID'], credentials.creds['CLIENT_SECRET']))
        all_stat.extend(stats.json())
    for x in all_stat:
        stuff['repos'].append(x['full_name'])
        if x['language'] in stuff['languages'].keys():
            stuff['languages'][x['language']] += 1 
        else:
            stuff['languages'][x['language']] = 1
    return json.dumps(stuff)

def comms(username):
    '''
    Grab summary stats from user repos
    '''
    commits = {}
    new_d = {}
    rep_link = grabber(username)['repos_url'] + simple +'?client_id={}&client_secret={}'.format( credentials.creds['CLIENT_ID'], credentials.creds['CLIENT_SECRET'])
    c = Get(rep_link)
    reps = c.json()
    while 'next' in c.links.keys():
        c = Get(c.links['next']['url'])
        reps.extend(c.json())
    commits['Day'],commits['Hour'] = {},{}
    for j in range(0,7):
        commits['Day'][j] = 0 
    for j in range (0,24):
        commits['Hour'][j]= 0 
    for a in reps:
        com_link = 'https://api.github.com/repos/{}/commits?author={}?client_id={}&client_secret={}'.format(a['full_name'], username, credentials.creds['CLIENT_ID'], credentials.creds['CLIENT_SECRET'])
        commit = Get(com_link ).json()
        # now foe the fun
        for t in commit:
            d = parser.parse(t['commit']['author']['date'])
            commits['Day'][d.weekday()] += 1
            commits['Hour'][d.hour] += 1 
    for m, l in zip(range(0,7), ['Monday', 'Tuesday', 'Wednesday',
                                  'Thursday', 'Friday', 'Saturday',
                                  'Sunday']):
        new_d[l] = commits['Day'][m]
    commits['Day']=new_d
    return json.dumps(commits)

def main():
    '''
    Return the things!
    '''
    uname = sys.argv[1]
    pull = sys.argv[2]
    if pull == 'stats':
        print(stats(uname))
    else:
        print(comms(uname))
    sys.stdout.flush()

if __name__ == '__main__':
    main()