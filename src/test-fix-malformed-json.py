import os
import pandas as pd
import re
import json
import boto3

path = os.getcwd() + "/"
files = [f for f in os.listdir() if re.match('canvas-live-events', f)]
files

df = pd.DataFrame
for f in files:
    df.append(pd.read_json(f, orient = 'records', lines = True))

with open(f) as file:
   data = json.load(file)

# My creds are dead
sess = boto3.session.Session(aws_access_key_id='XXX', aws_secret_access_key='YYY')
sess.get_available_services()
s3 = sess.resource('s3')
# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)



def try_correct_json(json_string):
  try:
    # First check if the json is okay.
    json.loads(json_string)
    return [json_string]
  except ValueError:
    try:
      # If not, try correcting it by adding a ending brace.
      try_to_correct_json = json_string + "}"
      json.loads(try_to_correct_json)
      return [try_to_correct_json]
    except ValueError:
      # The malformed json input can't be recovered, drop this input.
      return []

infile = open(f).read()

try_correct_json(infile)

l = []
for line in infile:

    l.append(json.loads(line))
