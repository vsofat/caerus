from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

@app.route("/")
def root():
     return render_template("landing.html")

@app.route("/homepage")
def homepage():
     return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run()