from utl.database.models.models import db, Scholarship, ScholarshipLink


def searchScholarships(query):
    like = "%" + query + "%"
    scholarships = (
        Scholarship.query.filter(
            (Scholarship.title.like(like)) | (Scholarship.description.like(like))
        )
        .order_by(Scholarship.datePosted.desc())
        .all()
    )
    for scholarship in scholarships:
        links = ScholarshipLink.query.filter_by(
            scholarshipID=scholarship.scholarshipID
        ).all()
        scholarship.links = [link.link for link in links]
    return query, scholarships
