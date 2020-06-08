from .models import db, Opportunity, OpportunityGrade, OpportunityLink, Scholarship, ScholarshipLink, Resource

def searchOpportunities(query):
    like = '%' + query + '%'
    opportunities = Opportunity.query.filter((Opportunity.title.like(like)) | (Opportunity.description.like(like))).all().order_by(Opportunity.datePosted.desc())
    for opportunity in opportunities:
        grades = OpportunityGrade.query.filter_by(
            opportunityID=opportunity.opportunityID
        ).all()
        opportunity.grades = [grade.grade for grade in grades]
        links = OpportunityLink.query.filter_by(
            opportunityID=opportunity.opportunityID
        ).all()
        opportunity.links = [link.link for link in links]
    return query, opportunities

def searchScholarships(query):
    like = '%' + query + '%'
    scholarships = Scholarship.query.filter((Scholarship.title.like(like)) | (Scholarship.description.like(like))).all().order_by(Scholarship.datePosted.desc())
    for scholarship in scholarships:
        links = ScholarshipLink.query.filter_by(
            scholarshipID=scholarship.scholarshipID
        ).all()
        scholarship.links = [link.link for link in links]
    return query, scholarships

def searchResources(query):
    like = '%' + query + '%'
    resources = Resource.query.filter((Resource.title.like(like)) | (Resource.description.like(like))).all().order_by(Resource.datePosted.desc())
    return query, resources