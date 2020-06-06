from flask import Flask, request, redirect, session, render_template, url_for, flash
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow

app = Flask(__name__)
app.secret_key = os.urandom(32)

DIR = os.path.dirname(__file__) or '.'
DIR += '/'


flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'oauth-client.json',
    ['https://www.googleapis.com/auth/userinfo.email',
     'https://www.googleapis.com/auth/userinfo.profile',
     'openid'])


flow.redirect_uri = 'http://127.0.0.1:5000/redirect'

authorization_url, state = flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
    access_type='offline',
    # Enable incremental authorization. Recommended as a best practice.
    include_granted_scopes='true')


@app.route('/')
def root():
    print(authorization_url)
    return redirect(authorization_url)
    # return render_template('index.html')


if __name__ == '__main__':
    app.debug = False
    app.run()
