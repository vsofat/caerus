from .models import db, Scholarship, ScholarshipLink


def getAllScholarships():
    scholarships = Scholarship.query.all()
    for scholarship in scholarships:
        scholarshipID = scholarship.scholarshipID
        scholarshipLinks = ScholarshipLink.query.filter_by(
            scholarshipID=scholarshipID
        ).all()
        scholarship.links = [
            scholarshipLinks.link for scholarshipLink in scholarshipLinks
        ]
    return scholarships


def getScholarship(scholarshipID):
    scholarship = Scholarship.query.filter_by(scholarshipID=scholarshipID).first()
    scholarshipLinks = ScholarshipLink.query.filter_by(
        scholarshipID=scholarshipID
    ).all()
    scholarship.links = [scholarshipLinks.link for scholarshipLink in scholarshipLinks]
    return scholarship


def createScholarship(body):
    title = body.title
    description = body.description
    deadline = body.deadline
    eligibility = body.eligibility
    datePosted = body.datePosted
    scholarship = Scholarship(
        title=title,
        description=description,
        deadline=deadline,
        eligibility=eligibility,
        datePosted=datePosted,
    )
    db.session.add(scholarship)
    db.session.commit()
