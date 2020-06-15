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
        return False
    else:
        opportunity = SavedOpportunity(
            userID=userID, opportunityID=opportunityID, reminderDate=None)
        db.session.add(opportunity)
        db.session.commit()
        return True


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
