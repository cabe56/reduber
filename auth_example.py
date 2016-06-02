# Setup auth to make requests
# See https://developer.uber.com/docs/authentication for brief explanation
from uber_rides.session import Session, OAuth2Credential

# These three auth-related vars can be found in the settings section of your app
# Go here for a list of your apps: https://developer.uber.com/dashboard
SERVER_TOKEN = 'vDQuJFj_x2JO-2ZsM9P_gCFZUTyOiPxqRj6jyUBB'
CLIENT_ID = '2oDvSKUmsHH2QB8Hgf-mJIPhY6UtsMgn'
CLIENT_SECRET = 'oItRmpHDjrZgXFKKMQ2T6loTtgX2G0yyczGauqll'

# Permissions required by this apps
# See all available at https://developer.uber.com/docs/scopes
PERMISSION_SCOPES = []

# Uber will use this url to redirect the user after confirmation is given
# that your app has permission to act on his behalf
REDIRECT_URL = 'mysite.com/already-signed-up-user'
# This is given by the oauth service
ACCESS_TOKEN = 'accessToken-34f21'
AUTHORIZATION_CODE_GRANT = 'object with o'
REFRESH_TOKEN = 'token used to get new access token after expiration'

oauth_credential = OAuth2Credential(
    client_id=CLIENT_ID,
    redirect_url=REDIRECT_URL,
    access_token=ACCESS_TOKEN,
    expires_in_seconds=52800,
    scopes=PERMISSION_SCOPES,
    grant_type=AUTHORIZATION_CODE_GRANT,
    client_secret=CLIENT_SECRET,
    refresh_token=REFRESH_TOKEN,
)

def get_session():
    return Session(oauth2credential=oauth_credential)

def uber_auth_url():
    """Return url where Uber will ask the user if we are allowed to make requests."""
    from uber_rides.auth import AuthorizationCodeGrant
    auth_flow = AuthorizationCodeGrant(
        CLIENT_ID,
        PERMISSION_SCOPES,
        CLIENT_SECRET,
        REDIRECT_URL,
    )
    return auth_flow.get_authorization_url()
