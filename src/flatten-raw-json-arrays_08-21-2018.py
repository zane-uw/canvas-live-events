#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 13:20:28 2018

@author: zane
"""

import os
import pandas as pd
# import re
import json
from pandas.io.json import json_normalize
import re

path = os.getcwd() + "/"

# =============================================================================

# with open('canvas live event sample') as f:
#     raw = f.read()

# spt_raw = raw.split('}{')
# spt_raw[1]

# spt_raw = re.split(r'(?<=}){', raw)

# will str.split work?
# I don't think so b/c there's nothing separating the entries
# blah = raw.split("}{")
# blah[0]
# blah[1]


# but what if there WERE something between the lines?
# raw2 = raw.replace("}{", "}\n{")
# raw2 = raw2.splitlines()

# spt_raw[1:] = ["{" + s for s in spt_raw[1:]]

# spt_raw[0]
# spt_raw[1]
# spt_raw[5]

# pj = [pd.read_json(s) for s in spt_raw]
# pj = [pd.read_json(s) for s in raw2]

# x = pj[0]['data']

# x = json_normalize(x)
# x.describe
# x.keys

# x['action']

# y = json_normalize(pj[5]['data'])
# y.head()

# y = json_normalize(data = pj[5]['data'])
# y.keys()
# y['actor.type']
# y['actor.extensions.com.instructure.canvas.entity_id']

# =============================================================================


# ok, all of that works, so:

with open('data/canvas-live-events-1-2018-04-06-02-42-07-7c2041f3-c597-4b4f-843a-e6ca668f0d6d') as f:
    raw = f.read()
len(raw)

raw = raw.replace("}{", "}\n{")
spt_raw = raw.splitlines()

spt_raw[0]

# nave = [x for x in spt_raw if "NavigationEvent" in x]
# ppl = [x for x in spt_raw if "100000003653431" in x]

js = [json.loads(line) for line in spt_raw]
# df = [pd.read_json(s) for s in spt_raw]

js[0]['data']
# jd = [j['data'] for j in js]
# jd[0]

# jd[0]['actor']
js[0]['data'][0]['actor']
# ok -

jd = [j['data'][0] for j in js]
# jd['actor']         # no
jd[0]['actor']      # yes

[j['actor'] for j in jd]        # yes, ok
# [j['actor']['user_login'] for j in jd]
type(jd[0])
jd[0].keys()

df = [json_normalize(j['data'][0]) for j in js]
df[0].keys()
[i.shape for i in df]
df[0]['action']

# compare:
y = jd[0]
x = df[0]
y['actor']['type']
x['actor.type']

# so, if df is a list of dataframes and I want to split them up by different categories or values
#

def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results


#
## try this...
# x = jd[0].items()
#
#
#
#
#def find_id(obj):
#    arr = []
#
#    def extract(obj, arr):
#        if isinstance(obj, dict):
#            for k, v in obj.items():
#


# =============================================================================
# tabulate top-level types
i = pd.Series([j['type'] for j in jd])
i.value_counts()
# =============================================================================

# =============================================================================
# anonymize the id's for HCDE students
#anon = jd[0:5]

# need to hash the entity_id and urn:instructure:canvas:user:...
#anon = jd.copy()
#for i in anon:
#    hash(i['actor']['id'])
#    hash(i['actor'][])
#

# =============================================================================

vals = re.findall('[0-9]{13}', raw)
vals = list(dict.fromkeys(vals))
hvals = [hash(v) for v in vals]
dvals = dict(zip(vals, hvals))
# dvals = dict(zz)
re.sub('[0-9]{13}', lambda x: dvals.get(x), raw)
anon = re.sub('[0-9]{13}', lambda x: dvals.get(x), raw)
# then:
spt_raw = anon.splitlines()
spt_raw[0]
js = [json.loads(line) for line in spt_raw]
extract_values(js, "id")
with open("anon-live-events.txt", "w") as outfile:
    json.dump(js, outfile)



# =============================================================================
# will find all occurences of a key, which isn't always desirable
def find(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result
# =============================================================================

