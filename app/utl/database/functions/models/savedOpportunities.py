from utl.database.models.models import db, SavedOpportunity
from .opportunities import getOpportunity


def getSavedOpportunities(userID):
    savedOpportunities = SavedOpportunity.query.filter_by(userID=userID).all()
    opportunities = []
    for savedOpportunity in savedOpportunities:
        opportunities.append(getOpportunity(savedOpportunity.opportunityID))
    return opportunities


def saveOpportunity(userID, opportunityID):
    exists = db.session.query(SavedOpportunity.query.filter(
        SavedOpportunity.userID == userID, SavedOpportunity.opportunityID == opportunityID).exists()).scalar()
    if exists:
        return "Could not favorite opportunity because user has already favorited this opportunity"
    else:
        opportunity = SavedOpportunity(
            userID=userID, opportunityID=opportunityID)
        db.session.add(opportunity)
        db.session.commit()
        return "Successfully favorited opportunity"


def unsaveOpportunity(userID, opportunityID):
    SavedOpportunity.query.filter_by(
        userID=userID, opportunityID=opportunityID
    ).delete()
    db.session.commit()


def addOpportunityReminder(userID, opportunityID, reminderDate):
    opportunity = SavedOpportunity.query.filter_by(
        userID=userID, opportunityID=opportunityID
    ).first()
    opportunity.reminderDate = reminderDate
    db.session.commit()


def removeOpportunityReminder(userID, opportunityID):
    opportunity = SavedOpportunity.query.filter_by(
        userID=userID, opportunityID=opportunityID
    ).first()
    opportunity.reminderDate = None
    db.session.commit()
