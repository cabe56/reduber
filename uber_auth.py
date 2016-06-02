# your callback url for oauth2 step 2
import os
import requests
from rauth import OAuth2Service

OAUTH2_REDIRECT_URI = 'http://localhost:8080/oauth/cb'
OAUTH2_AUTHORIZE_URL='https://login.uber.com/oauth/authorize'
OAUTH2_ACCESS_TOKEN_URL='https://login.uber.com/oauth/token'
APP_NAME='Chof para ancianos'

def get_tokens(code):
    """Return pair of oauth2 tokens (access, refresh).

    The access token is used in all requests for rides, but it
    has an expiration date. Once it expires, the refresh token should
    be used to request another access token.
    """
    parameters = {
      'redirect_uri': OAUTH2_REDIRECT_URI,
      'code': code,
      'grant_type': 'authorization_code',
    }
    response = requests.post(
      'https://login.uber.com/oauth/token',
      auth=(os.environ['UBER_CLIENT_ID'], os.environ['UBER_CLIENT_SECRET']),
      data=parameters,
    )
    data = response.json()
    return data['access_token'], data['refresh_token']

def generate_uber_login_url(api_base_url):
    """Return URL where Uber will ask user for permission to grant us access."""
    uber_api = OAuth2Service(
      client_id=os.environ['UBER_CLIENT_ID'],
      client_secret=os.environ['UBER_CLIENT_SECRET'],
      name=APP_NAME,
      authorize_url=OAUTH2_AUTHORIZE_URL,
      access_token_url=OAUTH2_ACCESS_TOKEN_URL,
      base_url=api_base_url
    )
    params = {
      'response_type': 'code',
      'redirect_uri': OAUTH2_REDIRECT_URI,
      # Permissions needed to see the user info and
      # request rides on their behalf
      'scope': 'profile request',
    }
    # Uber URL where user will authorize your application
    return uber_api.get_authorize_url(**params)
