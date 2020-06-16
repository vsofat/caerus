from utl.database.models.models import db, Scholarship, ScholarshipLink, SavedScholarship


def getAllScholarships():
    scholarships = Scholarship.query.order_by(
        Scholarship.datePosted.desc()).all()
    for scholarship in scholarships:
        links = ScholarshipLink.query.filter_by(
            scholarshipID=scholarship.scholarshipID
        ).all()
        scholarship.links = [link.link for link in links]
    return scholarships


def getScholarship(scholarshipID):
    scholarship = Scholarship.query.filter_by(
        scholarshipID=scholarshipID).first()
    links = ScholarshipLink.query.filter_by(
        scholarshipID=scholarshipID
    ).all()
    scholarship.links = [link.link for link in links]
    return scholarship


def createScholarship(body):
    scholarship = Scholarship(
        title=body['title'],
        description=body['description'],
        amount=body['amount'],
        deadline=body['deadline'],
        eligibility=body['eligibility'],
    )
    db.session.add(scholarship)
    db.session.commit()
    for link in body['links']:
        newLink = ScholarshipLink(
            scholarshipID=scholarship.scholarshipID, link=link)
        db.session.add(newLink)
    db.session.commit()

def editScholarship(body):
    scholarshipID = body['scholarshipID']
    scholarship = Scholarship.query.filter_by(scholarshipID=scholarshipID).first()
    scholarship.title = body['title']
    scholarship.description = body['description']
    scholarship.amount = body['amount']
    scholarship.deadline = body['deadline']
    scholarship.eligibility = body['eligibility']
    ScholarshipLink.query.filter_by(scholarshipID=scholarshipID).delete()
    for link in body['links']:
        newLink = ScholarshipLink(
            scholarshipID=scholarship.scholarshipID, link=link)
        db.session.add(newLink)
    db.session.commit()


def deleteScholarship(scholarshipID):
    Scholarship.query.filter_by(scholarshipID=scholarshipID).delete()
    ScholarshipLink.query.filter_by(scholarshipID=scholarshipID).delete()
    SavedScholarship.query.filter_by(scholarshipID=scholarshipID).delete()
    db.session.commit()
