from .models import db, Opportunity, OpportunityGrade, OpportunityLink


def getAllOpportunities():
    opportunities = Opportunity.query.all().order_by(Opportunity.datePosted.desc())
    for opportunity in opportunities:
        grades = OpportunityGrade.query.filter_by(
            opportunityID=opportunity.opportunityID).all()
        opportunity.grades = [grade.grade for grade in grades]
        links = OpportunityLink.query.filter_by(
            opportunityID=opportunity.opportunityID).all()
        opportunity.links = [link.link for link in links]
    return opportunities


def getOpportunity(opportunityID):
    opportunity = Opportunity.query.filter_by(
        opportuniyID=opportunityID).first()
    grades = OpportunityGrade.query.filter_by(
        opportunityID=opportunityID).all()
    links = OpportunityLink.query.filter_by(opportunityID=opportunityID).all()
    opportunity.grades = [grade.grade for grade in grades]
    opportunity.links = [link.link for link in links]
    return opportunity


def createOpportunity(body):
    opportunity = Opportunity(title=body.title, description=body.description, field=body.field, gender=body.gender,
                              location=body.location, startDate=body.startDate, endDate=body.endDate, deadline=body.deadline, cost=body.cost)
    db.session.add(opportunity)
    db.session.commit()
