from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Resources
class Resource(db.Model):
  resourceID = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String, nullable=False)
  description = db.Column(db.Text, nullable=False)  
  link = db.Column(db.String, nullable=False)

# Preferences
class FieldPreference(db.Model):
  fieldPreferenceID = db.Column(db.Integer, primary_key=True)
  userID = db.Column(db.Integer, nullable=False)
  field = db.Column(db.String, nullable=False)

class GradePreference(db.Model):
  gradePreferenceID = db.Column(db.Integer, primary_key=True)
  userID = db.Column(db.Integer, nullable=False)
  grade = db.Column(db.Integer, nullable=False)

class GenderPreference(db.Model):
  genderPreferenceID = db.Column(db.Integer, primary_key=True)
  userID = db.Column(db.Integer, nullable=False)
  gender = db.Column(db.String, nullable=False)

class CostPreference(db.Model):
  costPreferenceID = db.Column(db.Integer, primary_key=True)
  userID = db.Column(db.Integer, nullable=False)
  cost = db.Column(db.Float, nullable=False)
