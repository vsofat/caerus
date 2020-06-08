from .models import db, SavedOpportunity, SavedScholarship
from .opportunities import getOpportunity
from .scholarships import getScholarship


def getSavedOpportunities(userID):
    savedOpportunities = SavedOpportunity.query.filter_by(
        userID=userID).all()
    opportunities = []
    for savedOpportunity in savedOpportunities:
        opportunities.append(getOpportunity(savedOpportunity.opportunityID))
    return opportunities


def getSavedScholarships(userID):
    savedScholarships = SavedScholarship.query.filter_by(
        userID=userID).all()
    scholarships = []
    for savedScholarship in savedScholarships:
        scholarships.append(getScholarship(savedScholarship.scholarshipID))
    return scholarships


def saveOpportunity(userID, opportunityID):
    opportunity = SavedOpportunity(
        userID=userID,
        opportunityID=opportunityID
    )
    db.session.add(opportunity)
    db.session.commit()


def saveScholarship(userID, scholarshipID):
    scholarship = SavedScholarship(
        userID=userID,
        scholarshipID=scholarshipID
    )
    db.session.add(scholarship)
    db.session.commit()


def unsaveOpportunity(userID, opportunityID):
    SavedOpportunity.query.filter_by(
        userID=userID, opportunityID=opportunityID).delete()
    db.session.commit()


def unsaveScholarship(userID, scholarshipID):
    SavedScholarship.query.filter_by(
        userID=userID, scholarshipID=scholarshipID).delete()
    db.session.commit()


def addOpportunityReminder(userID, opportunityID, reminderDate):
    opportunity = SavedOpportunity.query.filter_by(
        userID=userID, opportunityID=opportunityID).first()
    opportunity.reminderDate = reminderDate
    db.session.commit()


def addScholarshipReminder(userID, scholarshipID, reminderDate):
    scholarship = SavedScholarship.query.filter_by(
        userID=userID, scholarshipID=scholarshipID).first()
    scholarship.reminderDate = reminderDate
    db.session.commit()


def removeOpportunityReminder(userID, opportunityID):
    opportunity = SavedOpportunity.query.filter_by(
        userID=userID, opportunityID=opportunityID).first()
    opportunity.reminderDate = None
    db.session.commit()


def removeScholarshipReminder(userID, scholarshipID):
    scholarship = SavedScholarship.query.filter_by(
        userID=userID, scholarshipID=scholarshipID).first()
    scholarship.reminderDate = None
    db.session.commit()
