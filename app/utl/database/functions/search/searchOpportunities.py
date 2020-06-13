from utl.database.models.models import (
    db,
    Opportunity,
    OpportunityGrade,
    OpportunityLink,
)


def searchOpportunities(query):
    like = "%" + query + "%"
    opportunities = (
        Opportunity.query.filter(
            (Opportunity.title.like(like)) | (Opportunity.description.like(like))
        )
        .order_by(Opportunity.datePosted.desc())
        .all()
    )
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
