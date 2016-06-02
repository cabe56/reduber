import os
import requests
from flask import Flask, request, redirect
from flask import render_template
from flask import json
from flask import session
from uber_auth import get_tokens, generate_uber_login_url

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
#UBER_API_URL_BASE = 'https://sandbox-api.uber.com/v1'
UBER_API_URL_BASE = 'https://api.uber.com/v1'

# @app.route('/session')
def test_session():
    """Return session contents to user.

    We store Uber tokens to make rides in the session object.
    """
    s = {
        'access_token': session.get('access_token'),
        'refresh_token': session.get('refresh_token')
    }
    return str(s)

@app.route('/')
def new_request():
    if 'access_token' in session:
        # We can request a ride on behalf of the user
        return render_template('new_request.html')
    else:
        # Send user to Uber's grant-permission-page
        login_url = generate_uber_login_url(UBER_API_URL_BASE)
        return redirect(login_url)

@app.route('/requests', methods=['POST'])
def create_request():
    """Calls Uber API to request a ride to the user's current location."""
    token = session.get('access_token')
    # TODO: error handling
    # No location given
    # Access token expired
    # Price surge
    # No cars available
    params = {
        "product_id": os.environ['DEFAULT_PRODUCT_ID'],
        "start_latitude": request.form.get('lat'),
        "start_longitude": request.form.get('lon')
    }
    response = requests.post(
        UBER_API_URL_BASE + '/requests',
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token},
        data=json.dumps(params)
    )
    request_id = response.json().get('request_id')
    if request_id:
        return redirect('/requests/' + request_id)
    else:
        abort(500)

@app.route('/requests/<request_id>', methods=['GET'])
def show_request(request_id):
    """Render information about the ride requested."""
    token = session.get('access_token')
    response = requests.get(
        UBER_API_URL_BASE + '/requests/' + request_id,
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token}
    )
    data = response.json()
    if not data['driver']:
        # 'waiting' stage between requesting a ride
        # and having Uber process the request
        # We cannot render the request's page because
        # details are not known until the request is processed by Uber
        return render_template('please_refresh.html')
    else:
        return render_template('show_request.html',
            user_name='Mimi',
            driver_name=data['driver']['name'],
            eta_in_minutes=data['eta'],
            driver_photo_url=data['driver']['picture_url'],
            driver_cel=data['driver']['phone_number']
        )

@app.route('/oauth/cb')
def get_tokens_and_redirect():
    """Store tokens retreived using code given by Uber after user granted permission.

    This is the oauth2 redirect. After a user grant's our app permission at Uber's site,
    Uber redirects the user to this url.
    """
    # Store access token in session
    session['access_token'], session['refresh_token'] = get_tokens(request.args.get('code'))
    return render_template('new_request.html')

if __name__ == "__main__":
    port = int(os.getenv('PORT', 80))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('THIS_IS_A_DEV_INSTANCE', False)
    app.run(host=host, port=port, debug=debug)
