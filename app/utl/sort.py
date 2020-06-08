from .models import db, Opportunity, OpportunityGrade, OpportunityLink, Scholarship, ScholarshipLink, Resource


def searchOpportunities(sort):
    opportunities = []
    if sort == 'dateposted-asc':
        opportunities = Opportunity.query.all().order_by(Opportunity.datePosted.asc())
    elif sort == 'dateposted-desc':
        opportunities = Opportunity.query.all().order_by(Opportunity.datePosted.desc())
    elif sort == 'deadline-asc':
        opportunities = Opportunity.query.all().order_by(Opportunity.deadline.asc())
    elif sort == 'deadline-desc':
        opportunities = Opportunity.query.all().order_by(Opportunity.deadline.desc())
    elif sort == 'cost-asc':
        opportunities = Opportunity.query.all().order_by(Opportunity.cost.asc())
    elif sort == 'cost-desc':
        opportunities = Opportunity.query.all().order_by(Opportunity.cost.desc())
    for opportunity in opportunities:
        grades = OpportunityGrade.query.filter_by(
            opportunityID=opportunity.opportunityID
        ).all()
        opportunity.grades = [grade.grade for grade in grades]
        links = OpportunityLink.query.filter_by(
            opportunityID=opportunity.opportunityID
        ).all()
        opportunity.links = [link.link for link in links]
    return sort, opportunities


def searchScholarships(sort):
    scholarships = []
    if sort == 'dateposted-asc':
        scholarships = Scholarship.query.all().order_by(Scholarship.datePosted.asc())
    elif sort == 'dateposted-desc':
        scholarships = Scholarship.query.all().order_by(Scholarship.datePosted.desc())
    elif sort == 'deadline-asc':
        scholarships = Scholarship.query.all().order_by(Scholarship.deadline.asc())
    elif sort == 'deadline-desc':
        scholarships = Scholarship.query.all().order_by(Scholarship.deadline.desc())
    elif sort == 'amount-asc':
        scholarships = Scholarship.query.all().order_by(Scholarship.amount.asc())
    elif sort == 'amount-desc':
        scholarships = Scholarship.query.all().order_by(Scholarship.amount.desc())
    for scholarship in scholarships:
        links = ScholarshipLink.query.filter_by(
            scholarshipID=scholarship.scholarshipID
        ).all()
        scholarship.links = [link.link for link in links]
    return sort, scholarships


def searchResources(sort):
    resources = []
    if sort == 'dateposted-asc':
        resources = Resource.query.all().order_by(Resource.datePosted.asc())
    elif sort == 'dateposted-desc':
        resources = Resource.query.all().order_by(Resource.datePosted.desc())
    return sort, resources
