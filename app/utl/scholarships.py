from .models import db, Scholarship, ScholarshipLink


def getAllScholarships():
    scholarships = Scholarship.query.all().order_by(Scholarship.datePosted.desc())
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
        title=body.title,
        description=body.description,
        deadline=body.deadline,
        eligibility=body.eligibility,
    )
    db.session.add(scholarship)
    db.session.commit()
    for link in body.links:
        newLink = ScholarshipLink(scholarshipID=scholarship.scholarshipID, link=link)
        db.session.add(newLink)
    db.session.commit()
