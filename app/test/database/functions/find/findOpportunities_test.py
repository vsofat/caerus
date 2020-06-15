from datetime import datetime, timedelta

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

    emptyBody4 = {
        "field": [],
        "maximum-cost": 300,
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
    filteredOpportunitiesQuery40 = filterOpportunities(baseQuery, emptyBody4)
    filteredOpportunities40 = filteredOpportunitiesQuery40.all()

    # Semi-empty filters
    filteredOpportunitiesQuery5 = filterOpportunities(baseQuery, semiEmptyBody1)
    filteredOpportunities5 = filteredOpportunitiesQuery5.all()
    filteredOpportunitiesQuery6 = filterOpportunities(baseQuery, semiEmptyBody2)
    filteredOpportunities6 = filteredOpportunitiesQuery6.all()
    filteredOpportunitiesQuery7 = filterOpportunities(baseQuery, semiEmptyBody3)
    filteredOpportunities7 = filteredOpportunitiesQuery7.all()
    filteredOpportunitiesQuery8 = filterOpportunities(baseQuery, semiEmptyBody4)
    filteredOpportunities8 = filteredOpportunitiesQuery8.all()

    # assert
    assert filteredOpportunities1 == [tOpportunity4]
    assert filteredOpportunities2 == [tOpportunity1, tOpportunity2, tOpportunity3, tOpportunity4]
    assert filteredOpportunities3 == [tOpportunity1, tOpportunity2, tOpportunity3, tOpportunity4]
    assert filteredOpportunities4 == [tOpportunity1, tOpportunity2, tOpportunity3, tOpportunity4]
    assert filteredOpportunities40 == []
    assert filteredOpportunities5 == [tOpportunity3, tOpportunity4]
    assert filteredOpportunities6 == [tOpportunity2, tOpportunity4]
    assert filteredOpportunities7 == [tOpportunity1, tOpportunity4]
    assert filteredOpportunities8 == [tOpportunity4]


def test_filterOpportunities1(session):
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
        cost=0,
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
        cost=50,
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
        cost=100,
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
        cost=200,
    )
    session.add(tOpportunity1)
    session.add(tOpportunity2)
    session.add(tOpportunity3)
    session.add(tOpportunity4)
    session.commit()

    semiEmptyBody1 = {
        "field": [],
        "maximum-cost": 0,
        "grade": [],
        "gender": [],
    }

    semiEmptyBody2 = {
        "field": [],
        "maximum-cost": 30,
        "grade": [],
        "gender": [],
    }

    semiEmptyBody3 = {
        "field": [],
        "maximum-cost": 50,
        "grade": [],
        "gender": [],
    }

    semiEmptyBody4 = {
        "field": [],
        "maximum-cost": 300,
        "grade": [],
        "gender": [],
    }
    
    # act
    filteredOpportunitiesQuery1 = filterOpportunities(baseQuery, semiEmptyBody1)
    filteredOpportunities1 = filteredOpportunitiesQuery1.all()
    filteredOpportunitiesQuery2 = filterOpportunities(baseQuery, semiEmptyBody2)
    filteredOpportunities2 = filteredOpportunitiesQuery2.all()
    filteredOpportunitiesQuery3 = filterOpportunities(baseQuery, semiEmptyBody3)
    filteredOpportunities3 = filteredOpportunitiesQuery3.all()
    filteredOpportunitiesQuery4 = filterOpportunities(baseQuery, semiEmptyBody4)
    filteredOpportunities4 = filteredOpportunitiesQuery4.all()
    print(hasFilters(semiEmptyBody1))
    print(filteredOpportunitiesQuery1)
    print(filteredOpportunities1)
    print(hasFilters(semiEmptyBody2))
    print(filteredOpportunities2)
    print(hasFilters(semiEmptyBody3))
    print(filteredOpportunities3)
    print(hasFilters(semiEmptyBody4))
    print(filteredOpportunities4)
    # assert
    assert filteredOpportunities1 == [tOpportunity1]
    assert filteredOpportunities2 == [tOpportunity1]
    assert filteredOpportunities3 == [tOpportunity1, tOpportunity2]
    assert filteredOpportunities4 == [tOpportunity1, tOpportunity2, tOpportunity3, tOpportunity4]


def test_sortOpportunities(session):
    # arrange
    costAscSortOption = "cost-asc"
    costDescSortOption = "cost-desc"
    deadlineAscSortOption = "deadline-asc"
    deadlineDescSortOption = "deadline-desc"
    datePostedAscSortOption = "dateposted-asc"
    datePostedDescSortOption = "dateposted-desc"

    baseQuery = Opportunity.query
    tOpportunity1 = Opportunity(
        title="ff",
        description="faf",
        field="ACADEMIC PROGRAMS",
        gender="CO-ED",
        location="NYC",
        startDate=datetime.today() + timedelta(days = 5),
        endDate=datetime.today() + timedelta(days = 6),
        deadline=datetime.today() + timedelta(days = 2),
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
        deadline=datetime.today() + timedelta(days=10),
        cost=500,
    )
    tOpportunity3 = Opportunity(
        title="hh",
        description="hah",
        field="PARKS, ZOOS, & NATURE",
        gender="CO-ED",
        location="NYC",
        startDate=datetime.today() + timedelta(days = 5),
        endDate=datetime.today() + timedelta(days = 5),
        deadline=datetime.today(),
        cost=1000,
    )
    tOpportunity4 = Opportunity(
        title="hh",
        description="hah",
        field="PARKS, ZOOS, & NATURE",
        gender="CO-ED",
        location="NYC",
        startDate=datetime.today() + timedelta(days = 1),
        endDate=datetime.today() + timedelta(days = 1),
        deadline=datetime.today() + timedelta(days = 1),
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
    tOpportunityLink7 = OpportunityLink(opportunityID=4, link="https:l.l")
    tOpportunityLink8 = OpportunityLink(opportunityID=4, link="https:m.m")
    session.add(tOpportunityLink1)
    session.commit()
    session.add(tOpportunityLink2)
    session.commit()
    session.add(tOpportunityLink3)
    session.commit()
    session.add(tOpportunityLink4)
    session.commit()
    session.add(tOpportunityLink5)
    session.commit()
    session.add(tOpportunityLink6)
    session.commit()
    session.add(tOpportunityLink7)
    session.commit()
    session.add(tOpportunityLink8)
    session.commit()

    # act
    # Empty
    sortedOpportunitiesQuery1 = sortOpportunities(baseQuery, None)
    sortedOpportunities1 = sortedOpportunitiesQuery1.all()
    sortedOpportunitiesQuery2 = sortOpportunities(baseQuery, "")
    sortedOpportunities2 = sortedOpportunitiesQuery2.all()
    sortedOpportunitiesQuery3 = sortOpportunities(baseQuery, "   ")
    sortedOpportunities3 = sortedOpportunitiesQuery3.all()

    # Non-empty
    sortedOpportunitiesQuery4 = sortOpportunities(baseQuery, costAscSortOption)
    sortedOpportunities4 = sortedOpportunitiesQuery4.all()
    sortedOpportunitiesQuery5 = sortOpportunities(baseQuery, costDescSortOption)
    sortedOpportunities5 = sortedOpportunitiesQuery5.all()
    sortedOpportunitiesQuery6 = sortOpportunities(baseQuery, deadlineAscSortOption)
    sortedOpportunities6 = sortedOpportunitiesQuery6.all()
    sortedOpportunitiesQuery7 = sortOpportunities(baseQuery, deadlineDescSortOption)
    sortedOpportunities7 = sortedOpportunitiesQuery7.all()
    sortedOpportunitiesQuery8 = sortOpportunities(baseQuery, datePostedAscSortOption)
    sortedOpportunities8 = sortedOpportunitiesQuery8.all()
    sortedOpportunitiesQuery9 = sortOpportunities(baseQuery, datePostedDescSortOption)
    sortedOpportunities9 = sortedOpportunitiesQuery9.all()

    print(sortedOpportunities6)

    # assert
    # TODO: Sorting by datePosted varies by which record was inserted first; insertion order is currently not controlled.
    # assert sortedOpportunities1 == [tOpportunity1, tOpportunity2, tOpportunity3, tOpportunity4]
    # assert sortedOpportunities2 == [tOpportunity1, tOpportunity2, tOpportunity3, tOpportunity4]
    # assert sortedOpportunities3 == [tOpportunity1, tOpportunity2, tOpportunity3, tOpportunity4]
    
    # cost
    assert sortedOpportunities4 == [tOpportunity1, tOpportunity2, tOpportunity4, tOpportunity3]
    assert sortedOpportunities5 == [tOpportunity3, tOpportunity1, tOpportunity2, tOpportunity4]

    # deadline
    assert sortedOpportunities6 == [tOpportunity3, tOpportunity4, tOpportunity1, tOpportunity2]
    assert sortedOpportunities7 == [tOpportunity2, tOpportunity1, tOpportunity4, tOpportunity3]

    # assert sortedOpportunities7
    # assert sortedOpportunities8 == [tOpportunity4, tOpportunity3, tOpportunity2, tOpportunity1]
    # assert sortedOpportunities9 == [tOpportunity1, tOpportunity2, tOpportunity3, tOpportunity4]


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


def test_findOpportunities(session):
    # arrange
    costAscSortOption = "cost-asc"
    costDescSortOption = "cost-desc"
    deadlineAscSortOption = "deadline-asc"
    deadlineDescSortOption = "deadline-desc"
    datePostedAscSortOption = "dateposted-asc"
    datePostedDescSortOption = "dateposted-desc"

    baseQuery = Opportunity.query
    tOpportunity1 = Opportunity(
        title="ff",
        description="faf",
        field="ACADEMIC PROGRAMS",
        gender="CO-ED",
        location="NYC",
        startDate=datetime.today() + timedelta(days = 5),
        endDate=datetime.today() + timedelta(days = 6),
        deadline=datetime.today() + timedelta(days = 2),
        cost=500,
    )
    tOpportunity2 = Opportunity(
        title="ff",
        description="gag",
        field="BUSINESS & JOBS",
        gender="CO-ED",
        location="NYC",
        startDate=datetime.today(),
        endDate=datetime.today(),
        deadline=datetime.today() + timedelta(days=10),
        cost=500,
    )
    tOpportunity3 = Opportunity(
        title="hh",
        description="hah",
        field="PARKS, ZOOS, & NATURE",
        gender="CO-ED",
        location="NYC",
        startDate=datetime.today() + timedelta(days = 5),
        endDate=datetime.today() + timedelta(days = 5),
        deadline=datetime.today(),
        cost=1000,
    )
    tOpportunity4 = Opportunity(
        title="ff",
        description="hah",
        field="PARKS, ZOOS, & NATURE",
        gender="CO-ED",
        location="NYC",
        startDate=datetime.today() + timedelta(days = 1),
        endDate=datetime.today() + timedelta(days = 1),
        deadline=datetime.today() + timedelta(days = 1),
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
    tOpportunityLink7 = OpportunityLink(opportunityID=4, link="https:l.l")
    tOpportunityLink8 = OpportunityLink(opportunityID=4, link="https:m.m")
    session.add(tOpportunityLink1)
    session.commit()
    session.add(tOpportunityLink2)
    session.commit()
    session.add(tOpportunityLink3)
    session.commit()
    session.add(tOpportunityLink4)
    session.commit()
    session.add(tOpportunityLink5)
    session.commit()
    session.add(tOpportunityLink6)
    session.commit()
    session.add(tOpportunityLink7)
    session.commit()
    session.add(tOpportunityLink8)
    session.commit()

    filters = {
        "field": [],
        "maximum-cost": 500,
        "grade": ["11", "12"],
        "gender": ["CO-ED", "FEMALE"],
    }

    # act
    # filter and sort
    filterSortOpportunitiesQuery1 = sortOpportunities(filterOpportunities(baseQuery, filters), deadlineDescSortOption)
    filterSortOpportunities1 = filterSortOpportunitiesQuery1.all()
    # search, filter, and sort
    searchFilterSortOpportunitiesQuery1 = sortOpportunities(filterOpportunities(searchOpportunities(baseQuery, "ff"), filters), deadlineAscSortOption)
    searchFilterSortOpportunities1 = searchFilterSortOpportunitiesQuery1.all()

    # filter and sort
    assert filterSortOpportunities1 == [tOpportunity2, tOpportunity4] 
    
    # search, filter, and sort
    assert searchFilterSortOpportunities1 == [tOpportunity4, tOpportunity2] 