from utl.database.models.models import db, SavedScholarship
from .scholarships import getScholarship


def getSavedScholarships(userID):
    savedScholarships = SavedScholarship.query.filter_by(userID=userID).all()
    scholarships = []
    for savedScholarship in savedScholarships:
        scholarships.append(getScholarship(savedScholarship.scholarshipID))
    return scholarships


def saveScholarship(userID, scholarshipID):
    exists = db.session.query(SavedScholarship.query.filter(
        SavedScholarship.userID == userID, SavedScholarship.scholarshipID == scholarshipID).exists()).scalar()
    if exists:
        return False
    else:
        scholarship = SavedScholarship(
            userID=userID, scholarshipID=scholarshipID)
        db.session.add(scholarship)
        db.session.commit()
        return True


def unsaveScholarship(userID, scholarshipID):
    SavedScholarship.query.filter_by(
        userID=userID, scholarshipID=scholarshipID
    ).delete()
    db.session.commit()


def addScholarshipReminder(userID, scholarshipID, reminderDate):
    scholarship = SavedScholarship.query.filter_by(
        userID=userID, scholarshipID=scholarshipID
    ).first()
    scholarship.reminderDate = reminderDate
    db.session.commit()


def removeScholarshipReminder(userID, scholarshipID):
    scholarship = SavedScholarship.query.filter_by(
        userID=userID, scholarshipID=scholarshipID
    ).first()
    scholarship.reminderDate = None
    db.session.commit()
