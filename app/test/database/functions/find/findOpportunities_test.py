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


def test_hasFilters():
    assert hasFilters(
        {
            "field": [
                "ACADEMIC PROGRAMS",
                "ENGINEERING, MATH, & CS",
                "MEDICAL & LIFE SCIENCES",
            ],
            "maximum-cost": 500,
            "grade": ["JUNIOR", "SENIOR"],
            "gender": ["CO-ED", "FEMALE"],
        }
    )

    assert hasFilters(
        {
            "field": [],
            "maximum-cost": 500,
            "grade": ["JUNIOR", "SENIOR"],
            "gender": ["CO-ED", "FEMALE"],
        }
    )

    assert (
        hasFilters({"field": [], "maximum-cost": None, "grade": [], "gender": [],})
        == False
    )

    assert (
        hasFilters({"field": [], "maximum-cost": "", "grade": [], "gender": [],})
        == False
    )


def test_searchOpportunities(session):
    # arrange
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

    # act
    # Non-empty
    searchOpportunitiesResultsNonEmpty = searchOpportunities(baseQuery, "hh").all()
    # None
    searchOpportunitiesResultsNone = searchOpportunities(baseQuery, None).all()
    # Empty
    searchOpportunitiesResultsEmpty = searchOpportunities(baseQuery, "").all()
    searchOpportunitiesResultsEmpty1 = searchOpportunities(baseQuery, "   ").all()

    # assert
    # Non-empty
    assert isinstance(searchOpportunitiesResultsNonEmpty, list)
    assert len(searchOpportunitiesResultsNonEmpty) == 2
    assert tOpportunity3 in searchOpportunitiesResultsNonEmpty
    assert tOpportunity4 in searchOpportunitiesResultsNonEmpty
    assert searchOpportunitiesResultsNonEmpty == [tOpportunity3, tOpportunity4]

    # None
    assert searchOpportunitiesResultsNone == [
        tOpportunity1,
        tOpportunity2,
        tOpportunity3,
        tOpportunity4,
    ]

    # Empty
    assert searchOpportunitiesResultsEmpty == [
        tOpportunity1,
        tOpportunity2,
        tOpportunity3,
        tOpportunity4,
    ]
    assert searchOpportunitiesResultsEmpty1 == [
        tOpportunity1,
        tOpportunity2,
        tOpportunity3,
        tOpportunity4,
    ]


def test_filterOpportunities(session):
    # arrange
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
        cost=1000,
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

    # Full
    body = {
        "field": ["ACADEMIC PROGRAMS", "PARKS, ZOOS, & NATURE",],
        "maximum-cost": 500,
        "grade": ["11", "12"],
        "gender": ["CO-ED", "FEMALE"],
    }

    # Empty
    emptyBody1 = {
        "field": [],
        "maximum-cost": None,
        "grade": [],
        "gender": [],
    }

    emptyBody2 = {
        "field": [],
        "maximum-cost": "",
        "grade": [],
        "gender": [],
    }

    emptyBody3 = {
        "field": [],
        "maximum-cost": "   ",
        "grade": [],
        "gender": [],
    }

    # Semi-empty
    semiEmptyBody1 = body = {
        "field": ["ACADEMIC PROGRAMS", "PARKS, ZOOS, & NATURE",],
        "maximum-cost": None,
        "grade": ["11", "12"],
        "gender": ["CO-ED", "FEMALE"],
    }

    semiEmptyBody2 = body = {
        "field": [],
        "maximum-cost": 500,
        "grade": ["11", "12"],
        "gender": ["CO-ED", "FEMALE"],
    }

    semiEmptyBody3 = body = {
        "field": ["ACADEMIC PROGRAMS", "PARKS, ZOOS, & NATURE",],
        "maximum-cost": 500,
        "grade": [],
        "gender": ["CO-ED", "FEMALE"],
    }

    semiEmptyBody4 = body = {
        "field": ["ACADEMIC PROGRAMS", "PARKS, ZOOS, & NATURE",],
        "maximum-cost": 500,
        "grade": ["11", "12"],
        "gender": [],
    }

    # act
    # Full filters
    filteredOpportunitiesQuery1 = filterOpportunities(baseQuery, body)
    filteredOpportunities1 = filteredOpportunitiesQuery1.all()

    # No filters
    # None
    filteredOpportunitiesQuery2 = filterOpportunities(baseQuery, emptyBody1)
    filteredOpportunities2 = filteredOpportunitiesQuery2.all()
    # ""
    filteredOpportunitiesQuery3 = filterOpportunities(baseQuery, emptyBody2)
    filteredOpportunities3 = filteredOpportunitiesQuery3.all()
    # "   "
    filteredOpportunitiesQuery4 = filterOpportunities(baseQuery, emptyBody3)
    filteredOpportunities4 = filteredOpportunitiesQuery4.all()

    # Semi-empty filters
    filteredOpportunitiesQuery5 = filterOpportunities(baseQuery, semiEmptyBody1)
    filteredOpportunities5 = filteredOpportunitiesQuery5.all()
    filteredOpportunitiesQuery6 = filterOpportunities(baseQuery, semiEmptyBody2)
    filteredOpportunities6 = filteredOpportunitiesQuery6.all()
    filteredOpportunitiesQuery7 = filterOpportunities(baseQuery, semiEmptyBody3)
    filteredOpportunities7 = filteredOpportunitiesQuery7.all()
    filteredOpportunitiesQuery8 = filterOpportunities(baseQuery, semiEmptyBody4)
    filteredOpportunities8 = filteredOpportunitiesQuery8.all()

    print(filteredOpportunities1)
    print(filteredOpportunities2)
    print(filteredOpportunities3)
    print(filteredOpportunities4)

    # assert
    assert filteredOpportunities1 == [tOpportunity4]
    assert filteredOpportunities2 == [tOpportunity1, tOpportunity2, tOpportunity3, tOpportunity4]
    assert filteredOpportunities3 == [tOpportunity1, tOpportunity2, tOpportunity3, tOpportunity4]
    assert filteredOpportunities4 == [tOpportunity1, tOpportunity2, tOpportunity3, tOpportunity4]
    # assert filteredOpportunities1 == [tOpportunity1, tOpportunity2, tOpportunity3, tOpportunity4]
    # assert False


def test_queries(session):
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

    orFilters = [
        or_(
            Opportunity.field == "ACADEMIC PROGRAMS",
            Opportunity.field == "BUSINESS & JOBS",
        ),
        Opportunity.cost <= 500,
        Opportunity.opportunityID == OpportunityGrade.opportunityID,
        or_(OpportunityGrade.grade == 12, OpportunityGrade.grade == 10),
        or_(Opportunity.gender == "CO-ED"),
    ]
    print(Opportunity.query.filter(and_(*orFilters)))
    print(Opportunity.query.filter(and_(*orFilters)).all())
    # assert False
