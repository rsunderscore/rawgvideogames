# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.


retrieving data using rawg api  - https://rawg.io/apidocs
#Kaggle got data from them so why not me
Free for personal use as long as you attribute RAWG as the source of the data and/or images and add an active hyperlink from every page where the data of RAWG is used.

results are paginated - keep following the next pointer to get everything
? is there a paramter that could be used to obtain larger page size
++ check: https://api.rawg.io/docs/
ANSWER = yes, page_size=# to determine page size
to get a specific page send page=
? what is the unit for page_size
"""

# EXAMPLES
# GET https://api.rawg.io/api/platforms?key=YOUR_API_KEY
# GET https://api.rawg.io/api/games?key=YOUR_API_KEY&dates=2019-09-01,2019-09-30&platforms=18,1,7

import requests
import json
import pandas as pd
import os
import matplotlib.pyplot as plt

pd.set_option('display.max_columns',20)#don't show ellipses
#read rawg api key from input or get from file 
#APIKEY = input('api key: ')

BASEURL = 'https://api.rawg.io/api/{}'
APINAMES = """creator-roles
creators
developers
games
genres
platforms
publishers
stores
tags""".splitlines()
#init
#make sure we're in the right place to read the apikey file
curpth = os.getcwd()
assert os.path.basename(curpth) == 'rawgvideogames'

with open(r'apikey.dontsync.txt','r') as f:
    lines = f.readline()

if len(lines) > 0:
    APIKEY = lines[:32]


def getfromrawg(apiname, params):
    """
    Build a RAWG api url from provided information and API key

    Parameters
    ----------
    apiname : string
        the name of the API to call .
    params : string 
        GET paramaters that can be passed as part of the url.

    Returns
    -------
    dataframe.

    """
    url = BASEURL+apiname+'?key='+APIKEY+'&'+params
    url = url.rstrip('&')#strip of any extra ampersands
    res = requests.get(url)
    
    # if the request wasn't successful - something went wrong
    if res.status_code != 200:
        assert False
    
    rc = res.content # this should be a json resopnse
    d = json.loads(rc)
    len(d)
    list(d.keys())
    # ['count', 'next', 'previous', 'results']
    len(d['results']) # for some reason this doesn't always agree with d['count']
    
    #print high level info about the json
    print(f"count of results: {d['count']}")
    #print(f"link to previous: {d['previous']}")
    #print(f"link to next: {d['next']}")
    
    assert d['count'] == 51 #count is the total number of all results - not current page
    
    
    # get the results into a datframe so we can begin to explore
    resdf = pd.DataFrame(d['results'])
    #resdf.info()
    return (d['previous'], d['next'], d['count'], resdf)

def getplatresult(url):
    """ get a typical result set for the platforms API
    
    """
    res = requests.get(url)
    
    # if the request wasn't successful - something went wrong
    if res.status_code != 200:
        assert False
    
    rc = res.content # this should be a json resopnse
    d = json.loads(rc)
    len(d)
    list(d.keys())
    # ['count', 'next', 'previous', 'results']
    len(d['results']) # for some reason this doesn't always agree with d['count']
    
    #print high level info about the json
    print(f"count of results: {d['count']}")
    #print(f"link to previous: {d['previous']}")
    #print(f"link to next: {d['next']}")
    
    assert d['count'] == 51 #count is the total number of all results - not current page
    
    
    # get the results into a datframe so we can begin to explore
    resdf = pd.DataFrame(d['results'])
    #resdf.info()
    return (d['previous'], d['next'], d['count'], resdf)

#(prv, nxt, cnt, df) = (d['previous'], d['next'], d['count'], resdf)

def getallplatforms():
    """
    Returns
    -------
    alldf : dataframe
        contains all the results for the platforms that were fetched 1 page at a time.

    """
    url = r"https://api.rawg.io/api/platforms?key={}".format(APIKEY)#&page_size=100
    #loop through all platform results
    cur = url
    alldf = pd.DataFrame()
    while True:
        (prv, nxt, cnt, df) = (None, None, None, None)
        (prv, nxt, cnt, df) = getplatresult(cur)
        alldf = alldf.append(df)
        if nxt != None:
            cur = nxt
        else:
            print('done getting all results')
            break
    
    if nxt == None:
        print('num')
    
    alldf.info()
    return alldf





