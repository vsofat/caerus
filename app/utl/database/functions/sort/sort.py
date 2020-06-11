from utl.database.models.models import db, Opportunity, OpportunityGrade, OpportunityLink, Scholarship, ScholarshipLink, Resource


def sortOpportunities(sort):
    opportunities = []
    if sort == 'dateposted-asc':
        opportunities = Opportunity.query.order_by(Opportunity.datePosted.asc()).all()
    elif sort == 'dateposted-desc':
        opportunities = Opportunity.query.order_by(Opportunity.datePosted.desc()).all()
    elif sort == 'deadline-asc':
        opportunities = Opportunity.query.order_by(Opportunity.deadline.asc()).all()
    elif sort == 'deadline-desc':
        opportunities = Opportunity.query.order_by(Opportunity.deadline.desc()).all()
    elif sort == 'cost-asc':
        opportunities = Opportunity.query.order_by(Opportunity.cost.asc()).all()
    elif sort == 'cost-desc':
        opportunities = Opportunity.query.order_by(Opportunity.cost.desc()).all()
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


def sortScholarships(sort):
    scholarships = []
    if sort == 'dateposted-asc':
        scholarships = Scholarship.query.order_by(Scholarship.datePosted.asc()).all()
    elif sort == 'dateposted-desc':
        scholarships = Scholarship.query.order_by(Scholarship.datePosted.desc()).all()
    elif sort == 'deadline-asc':
        scholarships = Scholarship.query.order_by(Scholarship.deadline.asc()).all()
    elif sort == 'deadline-desc':
        scholarships = Scholarship.query.order_by(Scholarship.deadline.desc()).all()
    elif sort == 'amount-asc':
        scholarships = Scholarship.query.order_by(Scholarship.amount.asc()).all()
    elif sort == 'amount-desc':
        scholarships = Scholarship.query.order_by(Scholarship.amount.desc()).all()
    for scholarship in scholarships:
        links = ScholarshipLink.query.filter_by(
            scholarshipID=scholarship.scholarshipID
        ).all()
        scholarship.links = [link.link for link in links]
    return sort, scholarships


def sortResources(sort):
    resources = []
    if sort == 'dateposted-asc':
        resources = Resource.query.order_by(Resource.datePosted.asc()).all()
    elif sort == 'dateposted-desc':
        resources = Resource.query.order_by(Resource.datePosted.desc()).all()
    return sort, resources
