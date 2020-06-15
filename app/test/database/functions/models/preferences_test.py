from datetime import datetime, timedelta

from utl.database.models.models import User, Opportunity, FieldPreference, GradePreference, GenderPreference, CostPreference
from utl.database.functions.models.preferences import *

def test_createCostPreference(session):
    # arrange

    # act
    createCostPreference(1, 400)

    # assert
    assert CostPreference.query.filter(CostPreference.userID == 1).one()
    assert CostPreference.query.filter(CostPreference.userID == 1).one().cost == 400
    assert CostPreference.query.count() == 1


def test_updateCostPreference(session):
    # arrange

    # act
    createCostPreference(1, 400)
    updateCostPreference(1, 500)

    # assert
    assert CostPreference.query.filter(CostPreference.userID == 1).one()
    assert CostPreference.query.filter(CostPreference.userID == 1).one().cost == 500
    assert CostPreference.query.count() == 1


def test_getCostPreferences(session):
    baseQuery = Opportunity.query
    tOpportunity1 = Opportunity(
        title="ff",
        description="faf",
        field="ACADEMIC PROGRAMS",
        gender="CO-ED",
        location="NYC",
        startDate=datetime.today(),
        endDate=datetime.today(),
        deadline=datetime.today(),
        cost=500,
    )
    tOpportunity2 = Opportunity(
        title="gg",
        description="gag",
        field="BUSINESS & JOBS",
        gender="CO-ED",
        location="NYC",
        startDate=datetime.today(),
        endDate=datetime.today(),
        deadline=datetime.today(),
        cost=500,
    )
    tOpportunity3 = Opportunity(
        title="hh",
        description="hah",
        field="PARKS, ZOOS, & NATURE",
        gender="CO-ED",
        location="NYC",
        startDate=datetime.today(),
        endDate=datetime.today(),
        deadline=datetime.today(),
        cost=500,
    )
    tOpportunity4 = Opportunity(
        title="hh",
        description="hah",
        field="PARKS, ZOOS, & NATURE",
        gender="CO-ED",
        location="NYC",
        startDate=datetime.today(),
        endDate=datetime.today(),
        deadline=datetime.today(),
        cost=500,
    )
    session.add(tOpportunity1)
    session.add(tOpportunity2)
    session.add(tOpportunity3)
    session.add(tOpportunity4)
    session.commit()

    user1 = User(userID=1, email="f", name="f", imglink="f", userType="f", accessToken="f", refreshToken="f")
    session.add(user1)
    print(user1.userID)
    print(getPreferredOpportunities(1))
    locatedOpportunities = getPreferredOpportunities(1)

    assert isinstance(locatedOpportunities, list)
    assert len(locatedOpportunities) == 4
    assert tOpportunity1 in locatedOpportunities
    assert tOpportunity2 in locatedOpportunities
    assert tOpportunity3 in locatedOpportunities
    assert tOpportunity4 in locatedOpportunities