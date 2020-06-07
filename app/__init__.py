from flask import Flask, request, redirect, session, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
import json
import requests
import functools
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from utl import models

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

db = models.db
app = Flask(__name__)
app.secret_key = os.urandom(32)

DIR = os.path.dirname(__file__) or '.'
DIR += '/'

CLIENT_SECRETS_FILE = DIR + '../oauth-client.json'
SCOPES = ['https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/userinfo.profile',
          'openid']


def protected(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if 'credentials' in session:
            return f(*args, **kwargs)
        else:
            flash("You are not logged in", 'error')
            return redirect(url_for('root'))
    return wrapper


@app.route("/")
def root():
    if 'credentials' in session:
        credentials = dict_to_credentials(session['credentials'])
        session['credentials'] = credentials_to_dict(credentials)
        print('here')
        return redirect(url_for('opportunities'))
    else:
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
    return redirect(authorization_url)


@app.route("/redirect")
def oauthcallback():
    users = open(DIR + "static/data/users.json")
    users = json.load(users)

    teachers = users['teacher']
    admin = users['admin']

    org = request.args.get("hd")

    state = session['state'] if 'state' in session else None

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

    credentials = dict_to_credentials(session['credentials'])

    info = build('oauth2', 'v2', credentials=credentials)
    info = info.userinfo().get().execute()

    userid = info['id']
    email = info['email']
    name = info['name']
    picture = info['picture']

    if email in admin:
        usertype = 'admin'
    elif email in teachers:
        usertype = 'teacher'
    elif org == "stuy.edu":
        usertype = 'student'
    else:
        del session['credentials']
        flash("Please use an appropriate email", 'error')
        return redirect(url_for("root"))

    # print(info)
    # print(userid, email, name, picture, usertype)

    return redirect(url_for('opportunities'))


@app.route("/logout")
def logout():
    if 'credentials' not in session:
        return redirect(url_for('root'))

    credentials = dict_to_credentials(session['credentials'])

    revoke = requests.post('https://oauth2.googleapis.com/revoke',
                           params={'token': credentials.token},
                           headers={'content-type': 'application/x-www-form-urlencoded'})

    del session['credentials']

    return redirect(url_for('root'))


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def dict_to_credentials(dict):
    return google.oauth2.credentials.Credentials(
        dict['token'],
        dict['refresh_token'],
        dict['token_uri'],
        dict['client_id'],
        dict['client_secret'],
        dict['scopes']
    )


@app.route("/opportunities")
@protected
def opportunities():
    return render_template("index.html")


@app.route("/opportunities/<opportunityID>")
@protected
def opportunity(opportunityID):
    return render_template("individual.html")


@app.route("/scholarships")
@protected
def scholarships():
    return 'placeholder'


@app.route("/scholarships/<scholarshipID>")
@protected
def scholarship():
    return 'placeholder'


@app.route("/favorites")
@protected
def favorites():
    return 'placeholder'


@app.route("/resources")
@protected
def resources():
    return 'placeholder'


@app.route("/preferences")
@protected
def preferences():
    return 'placeholder'


if __name__ == "__main__":
    if not os.path.exists(CLIENT_SECRETS_FILE):
        print('Missing Google OAuth 2.0 Client ID file.')
        print('Read README.md for instructions')
        exit()
    app.debug = True
    app.run()
