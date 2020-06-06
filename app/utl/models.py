from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Opportunities
class Opportunity(db.Model):
    opportunityID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    field = db.Column(db.String, nullable=False)
    gender = db.Column(db.String)
    location = db.Column(db.String)
    startDate = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)
    deadline = db.Column(db.DateTime)
    cost = db.Column(db.Float, nullable=False)
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class OpportunityGrade(db.Model):
    opportunityID = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.Integer, nullable=False)


class OpportunityLink(db.Model):
    opportunityID = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String, nullable=False)


# Scholarships
class Scholarship(db.Model):
    scholarshipID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    eligibility = db.Column(db.String, nullable=False)
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class ScholarshipLink(db.Model):
    scholarshipID = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String, nullable=False)


# Saved
class SavedOpportunity(db.Model):
    userID = db.Column(db.Integer, nullable=False)
    opportunityID = db.Column(db.Integer, nullable=False)
    reminderDate = db.Column(db.DateTime)


class SavedScholarship(db.Model):
    userID = db.Column(db.Integer, nullable=False)
    scholarshipID = db.Column(db.Integer, nullable=False)
    reminderDate = db.Column(db.DateTime)


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
