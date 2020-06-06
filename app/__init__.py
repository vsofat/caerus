from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

# LANDING PAGE
@app.route("/")
def root():
     return render_template("landing.html")
     # eventually, will go to some kind of homepage or redirect to opportunity bulletin if logged in already

# OPPORTUNITY BULLETIN
@app.route("/opportunities")
def opportunities():
     return render_template("index.html")

# INDIVIDUAL OPPORTUNITY
@app.route("/opportunities/<opportunityID>")
def opportunity(opportunityID):
    return render_template("individual.html")

# SCHOLARSHIP FINDER
@app.route("/scholarships")
def scholarships():
    return 'placeholder'

# INDIVIDUAL SCHOLARSHIP
@app.route("/scholarships/<scholarshipID>")
def scholarship():
    return 'placeholder'

# FAVORITES/SAVED
@app.route("/favorites")
def favorites():
    return 'placeholder'

# RESOURCES
@app.route("/resources")
def resources():
    return 'placeholder'

# PREFERENCES
@app.route("/preferences")
def preferences():
    return 'placeholder'

if __name__ == "__main__":
    app.debug = True
    app.run()