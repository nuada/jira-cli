#!/usr/bin/env python
# usage: jira-cli.py <server_url>

import json
import sys

from oauthlib.oauth1 import SIGNATURE_RSA
from requests_oauthlib import OAuth1Session


def read(file_path):
    with open(file_path) as f:
        return f.read()

JIRA_SERVER = sys.argv[1]
CONSUMER_KEY = 'jira-cli'
RSA_KEY = read('private_key.pem')

REQUEST_TOKEN_URL = JIRA_SERVER + '/plugins/servlet/oauth/request-token'
AUTHORIZE_URL = JIRA_SERVER + '/plugins/servlet/oauth/authorize'
ACCESS_TOKEN_URL = JIRA_SERVER + '/plugins/servlet/oauth/access-token'

# Step 1: Get a request token
oauth = OAuth1Session(CONSUMER_KEY,
                      signature_type='auth_header',
                      signature_method=SIGNATURE_RSA,
                      rsa_key=RSA_KEY)
request_token = oauth.fetch_request_token(REQUEST_TOKEN_URL)

# Step 2: Get the end-user's authorization
print("Visit the following URL to provide authorization:")
print("  {}".format(oauth.authorization_url(AUTHORIZE_URL)))
while raw_input("Press any key to continue..."):
    pass

# Step 3: Get the access token and create config
access_token = oauth.fetch_access_token(ACCESS_TOKEN_URL)
with open('config.json', 'w') as f:
    json.dump(dict(server=JIRA_SERVER,
                   access_token=access_token['oauth_token'],
                   access_token_secret=access_token['oauth_token_secret'],
                   consumer_key=CONSUMER_KEY), f)
