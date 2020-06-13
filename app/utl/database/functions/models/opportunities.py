from utl.database.models.models import db, Opportunity, OpportunityGrade, OpportunityLink


def getAllOpportunities():
    opportunities = Opportunity.query.order_by(Opportunity.datePosted.desc()).all()
    for opportunity in opportunities:
        grades = OpportunityGrade.query.filter_by(
            opportunityID=opportunity.opportunityID
        ).all()
        opportunity.grades = [grade.grade for grade in grades]
        links = OpportunityLink.query.filter_by(
            opportunityID=opportunity.opportunityID
        ).all()
        opportunity.links = [link.link for link in links]
    return opportunities


def getOpportunity(opportunityID):
    opportunity = Opportunity.query.filter_by(
        opportunityID=opportunityID).first()
    grades = OpportunityGrade.query.filter_by(
        opportunityID=opportunityID).all()
    links = OpportunityLink.query.filter_by(opportunityID=opportunityID).all()
    opportunity.grades = [grade.grade for grade in grades]
    opportunity.links = [link.link for link in links]
    return opportunity


def createOpportunity(body):
    opportunity = Opportunity(
        title=body['title'],
        description=body['description'],
        field=body['field'],
        gender=body['gender'],
        location=body['location'],
        startDate=body['startDate'],
        endDate=body['endDate'],
        deadline=body['deadline'],
        cost=body['cost'],
    )
    db.session.add(opportunity)
    db.session.commit()
    for grade in body['grades']:
        newGrade = OpportunityGrade(
            opportunityID=opportunity.opportunityID, grade=grade)
        db.session.add(newGrade)
    for link in body['links']:
        newLink = OpportunityLink(
            opportunityID=opportunity.opportunityID, link=link)
        db.session.add(newLink)
    db.session.commit()


def deleteOpportunity(opportunityID):
    Opportunity.query.filter_by(opportunityID=opportunityID).delete()
    db.session.commit()
