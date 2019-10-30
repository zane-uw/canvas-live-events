import os
import pandas as pd
import re
import json
import boto3
from boto3 import Session

#path = os.getcwd() + "/"
#files = [f for f in os.listdir() if re.match('test-canvas-live-events', f)]
#files
#
#df = pd.DataFrame
#for f in files:
#    df.append(pd.read_json(f, orient = 'records', lines = True))
#
#with open(f) as file:
#   data = json.load(file)

session = Session()
credentials = session.get_credentials()
# Credentials are refreshable, so accessing your access key / secret key
# separately can lead to a race condition. Use this to get an actual matched
# set.
current_credentials = credentials.get_frozen_credentials()

session.get_available_resources()
session.get_available_services()


s3 = session.resource('s3')
# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)