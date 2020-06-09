from flask import Flask, request, redirect, session, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os
import json
import requests
import functools
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from utl import models, opportunities, preferences, resources, saved, scholarships, users
import datetime

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

db = models.db
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(32)

DIR = os.path.dirname(__file__) or '.'
DIR += '/'

CLIENT_SECRETS_FILE = DIR + '../oauth-client.json'
SCOPES = ['https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/userinfo.profile',
          'openid']

f = open(CLIENT_SECRETS_FILE)
f = json.load(f)['web']
TOKEN_URI = f['token_uri']
CLIENT_ID = f['client_id']
CLIENT_SECRET = f['client_secret']


def protected(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if 'userid' in session:
            return f(*args, **kwargs)
        else:
            flash("You are not logged in!", 'error')
            return redirect(url_for('root'))
    return wrapper


def staffonly(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        u = users.getUserInfo(session['userid'])
        if u.userType == 'admin' or u.userType == 'teacher':
            return f(*args, **kwargs)
        else:
            flash("You are not authorized!", 'error')
            return redirect(url_for('root'))
    return wrapper


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


@app.route("/")
def root():
    if 'userid' in session:
        userid = session['userid']
        access, refresh = users.getTokens(userid)
        credentials = dict_to_credentials({
            'token': access,
            'refresh_token': refresh,
            'token_uri': TOKEN_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'scopes': SCOPES
        })
        users.updateTokens(userid, credentials.token,
                           credentials.refresh_token)
        return redirect(url_for('opportunitiesRoute'))
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
    userfile = open(DIR + "static/data/users.json")
    userDict = json.load(userfile)

    teachers = userDict['teacher']
    admin = userDict['admin']

    org = request.args.get("hd")

    state = session['state'] if 'state' in session else None

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauthcallback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials

    info = build('oauth2', 'v2', credentials=credentials)
    info = info.userinfo().get().execute()

    email = info['email']
    userid = info['id']

    if email in admin:
        usertype = 'admin'
    elif email in teachers:
        usertype = 'teacher'
    elif org == "stuy.edu":
        usertype = 'student'
    else:
        flash("Please use an appropriate email", 'error')
        return redirect(url_for("root"))

    if users.userExists(userid):
        users.updateTokens(
            userid,
            credentials.token,
            credentials.refresh_token
        )
    else:
        users.createUser(
            userid,
            email,
            info['name'],
            info['picture'],
            usertype,
            credentials.token,
            credentials.refresh_token
        )

    session['userid'] = userid

    return redirect(url_for('opportunitiesRoute'))


@app.route("/logout")
def logout():
    if 'userid' not in session:
        return redirect(url_for('root'))

    userid = session['userid']

    access, refresh = users.getTokens(userid)

    revoke = requests.post('https://oauth2.googleapis.com/revoke',
                           params={'token': access},
                           headers={'content-type': 'application/x-www-form-urlencoded'})

    users.nullifyTokens(userid)

    del session['userid']

    return redirect(url_for('root'))


@app.route("/opportunities")
@protected
def opportunitiesRoute():
    return render_template("opportunities.html",
                           user=users.getUserInfo(session['userid']),
                           opportunityList=opportunities.getAllOpportunities()
                           )


@app.route("/opportunities/<opportunityID>")
@protected
def opportunityRoute(opportunityID):
    return render_template("individual.html", opp=opportunities.getOpportunity(opportunityID)
                           )


def strtodate(string):
    if len(string) > 0:
        return datetime.datetime.strptime(string, '%Y-%m-%d')
    else:
        return None


@app.route("/opportunities/create", methods=['GET', 'POST'])
@protected
@staffonly
def createOpportunityRoute():
    if (request.method == 'GET'):
        return render_template('createopportunity.html')
    elif (request.method == 'POST'):
        links = list()
        grades = list()
        f = request.form
        for key in f.keys():
            if 'link' in key:
                links.append(request.form[key])
            if 'grades' == key:
                grades = request.form[key].split(',')
        location = request.form['location']
        location = location if len(location) > 0 else None
        opportunities.createOpportunity({
            'title': request.form['title'],
            'description': request.form['description'],
            'field': request.form['field'],
            'gender': request.form['gender'],
            'location': location,
            'startDate': strtodate(request.form['start']),
            'endDate': strtodate(request.form['end']),
            'deadline': strtodate(request.form['deadline']),
            'cost': request.form['cost'],
            'grades': grades,
            'links': links
        })
        flash("Successfully created an opportunity", 'success')
        return render_template('createopportunity.html')


@app.route("/scholarships")
@protected
def scholarshipsRoute():
    return render_template("scholarships.html",
                           user=users.getUserInfo(session['userid']),
                           scholars=scholarships.getAllScholarships()
                           )


@app.route("/scholarships/<scholarshipID>")
@protected
def scholarshipRoute():
    return render_template("individual.html")


@app.route("/scholarships/create", methods=['GET', 'POST'])
@protected
@staffonly
def createScholarshipRoute():
    if (request.method == 'GET'):
        return render_template('createscholarship.html')
    elif (request.method == 'POST'):
        # links = list()
        # grades = list()
        # f = request.form
        # for key in f.keys():
        #     if 'link' in key:
        #         links.append(request.form[key])
        #     if 'grades' == key:
        #         grades = request.form[key].split(',')
        # location = request.form['location']
        # location = location if len(location) > 0 else None
        # opportunities.createOpportunity({
        #     'title': request.form['title'],
        #     'description': request.form['description'],
        #     'field': request.form['field'],
        #     'gender': request.form['gender'],
        #     'location': location,
        #     'startDate': strtodate(request.form['start']),
        #     'endDate': strtodate(request.form['end']),
        #     'deadline': strtodate(request.form['deadline']),
        #     'cost': request.form['cost'],
        #     'grades': grades,
        #     'links': links
        # })
        flash("Successfully created a scholarship", 'success')
        return render_template('createscholarship.html')


@app.route("/resources")
@protected
def resourcesRoute():
    return render_template("resources.html",
                           user=users.getUserInfo(session['userid']),
                           res=resources.getAllResources())


@app.route("/resources/create")
@protected
def resourceRoute():
    return render_template("createResources.html",
                           user=users.getUserInfo(session['userid']),
                           res=resources.getAllResources())


@app.route("/favorites")
@protected
def favoritesRoute():
    return render_template("favorites.html",
                           user=users.getUserInfo(session['userid']))


@app.route("/preferences")
@protected
def preferencesRoute():
    return render_template("preferences.html",
                           user=users.getUserInfo(session['userid']))


@app.route('/dumb')
def dumb():
    newOpp = {
        'title': 'yo momma',
        'description': 'at my house last nite!!! #yolo',
        'field': 'STEM',
        'gender': None,
        'location': '106 W 117th Street, New York, NY, 10026',
        'startDate': datetime.datetime.today(),
        'endDate': None,
        'deadline': None,
        'cost': 0,
        'grades': [9, 10, 11, 12],
        'links': ['hello'],
    }
    opportunities.createOpportunity(newOpp)
    return 'submitted'


if __name__ == "__main__":
    if not os.path.exists(CLIENT_SECRETS_FILE):
        print('Missing Google OAuth 2.0 Client ID file.')
        print('Read README.md for instructions.')
        exit()
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.debug = True
    app.run()
