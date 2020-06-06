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