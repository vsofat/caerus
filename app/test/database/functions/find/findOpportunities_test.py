from datetime import datetime

from sqlalchemy import and_, or_

from utl.database.models.models import Opportunity, OpportunityGrade, OpportunityLink
from utl.database.functions.find.findOpportunities import (
    hasFilters,
    searchOpportunities,
    filterOpportunities,
    sortOpportunities,
    findOpportunities,
)

def test_filterOpportunities(session):
    tOpportunity1 = Opportunity(title="ff", description="faf", field="Academic Programs", gender="CO-ED", location="NYC", startDate=datetime.today(), endDate=datetime.today(), deadline=datetime.today(), cost=500)
    tOpportunity2 = Opportunity(title="gg", description="gag", field="Business & Jobs", gender="CO-ED", location="NYC", startDate=datetime.today(), endDate=datetime.today(), deadline=datetime.today(), cost=500)
    tOpportunity3 = Opportunity(title="hh", description="hah", field="Parks, Zoos, & Nature", gender="CO-ED", location="NYC", startDate=datetime.today(), endDate=datetime.today(), deadline=datetime.today(), cost=500)
    tOpportunity4 = Opportunity(title="hh", description="hah", field="Parks, Zoos, & Nature", gender="CO-ED", location="NYC", startDate=datetime.today(), endDate=datetime.today(), deadline=datetime.today(), cost=500)
    session.add(tOpportunity1)
    session.add(tOpportunity2)
    session.add(tOpportunity3)
    session.add(tOpportunity4)
    session.commit()

    # Opportunity grades
    tOpportunityGrade1 = OpportunityGrade(opportunityID=1, grade="9")
    tOpportunityGrade2 = OpportunityGrade(opportunityID=1, grade="10")
    tOpportunityGrade3 = OpportunityGrade(opportunityID=2, grade="12")
    tOpportunityGrade4 = OpportunityGrade(opportunityID=2, grade="11")
    tOpportunityGrade5 = OpportunityGrade(opportunityID=3, grade="9")
    tOpportunityGrade6 = OpportunityGrade(opportunityID=3, grade="12")
    tOpportunityGrade7 = OpportunityGrade(opportunityID=4, grade="12")
    tOpportunityGrade8 = OpportunityGrade(opportunityID=4, grade="12")
    session.add(tOpportunityGrade1)
    session.add(tOpportunityGrade2)
    session.add(tOpportunityGrade3)
    session.add(tOpportunityGrade4)
    session.add(tOpportunityGrade5)
    session.add(tOpportunityGrade6)
    session.add(tOpportunityGrade7)
    session.add(tOpportunityGrade8)
    session.commit()
    
    # Opportunity links
    tOpportunityLink1 = OpportunityLink(opportunityID=1, link="https:f.f")
    tOpportunityLink2 = OpportunityLink(opportunityID=1, link="https:g.g")
    tOpportunityLink3 = OpportunityLink(opportunityID=2, link="https:h.h")
    tOpportunityLink4 = OpportunityLink(opportunityID=2, link="https:i.i")
    tOpportunityLink5 = OpportunityLink(opportunityID=3, link="https:j.j")
    tOpportunityLink6 = OpportunityLink(opportunityID=3, link="https:k.k")
    session.add(tOpportunityLink1)
    session.add(tOpportunityLink2)
    session.add(tOpportunityLink3)
    session.add(tOpportunityLink4)
    session.add(tOpportunityLink5)
    session.add(tOpportunityLink6)
    session.commit()

    orFilters = [or_(Opportunity.field == "Academic Programs", Opportunity.field == "Business & Jobs"), Opportunity.cost <= 500, Opportunity.opportunityID == OpportunityGrade.opportunityID, OpportunityGrade.grade == 12, or_(Opportunity.gender == "CO-ED")]
    print(Opportunity.query.filter(and_(*orFilters)))
    print(Opportunity.query.filter(and_(*orFilters)).all())
    print(Opportunity.query.filter().all())
    assert False