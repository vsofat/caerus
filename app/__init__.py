from flask import Flask, request, redirect, session, render_template, url_for, flash
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow

import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = os.urandom(32)

DIR = os.path.dirname(__file__) or '.'
DIR += '/'

CLIENT_SECRETS_FILE = DIR + '../oauth-client.json'
SCOPES = ['https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/userinfo.profile',
          'openid']


# LANDING PAGE
@app.route("/")
def root():
    return render_template("landing.html")


@app.route("/auth")
def auth():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)

    flow.redirect_uri = 'http://127.0.0.1:5000/redirect'

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    session['state'] = state
    print("STATE", state)
    return redirect(authorization_url)


@app.route("/redirect")
def oauthcallback():
    org = request.args.get("hd")
    if not org == "stuy.edu":
        flash("Please use your stuy.edu email", 'error')
        return redirect(url_for("root"))

    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauthcallback', _external=True)

    authorization_response = request.url
    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('opportunities'))


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


@app.route("/opportunities")
def opportunities():
    return render_template("index.html")


@app.route("/opportunities/<opportunityID>")
def opportunity(opportunityID):
    return render_template("individual.html")


@app.route("/scholarships")
def scholarships():
    return 'placeholder'


@app.route("/scholarships/<scholarshipID>")
def scholarship():
    return 'placeholder'


@app.route("/favorites")
def favorites():
    return 'placeholder'


@app.route("/resources")
def resources():
    return 'placeholder'


@app.route("/preferences")
def preferences():
    return 'placeholder'


if __name__ == "__main__":
    app.debug = True
    app.run()
