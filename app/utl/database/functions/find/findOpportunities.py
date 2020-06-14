from sqlalchemy import and_, or_

from utl.database.models.models import (
    Opportunity,
    OpportunityGrade,
    OpportunityLink,
)


def hasFilters(filters):
    """
    input:
    {field: ["ACADEMIC PROGRAMS", "ENGINEERING, MATH, & CS", "MEDICAL & LIFE SCIENCES"],
        maximum-cost: 500, grade: ["JUNIOR", "SENIOR"], gender: ["CO-ED", "FEMALE"]}
    output:
    True or False
    """
    return (
        len(filters["field"])
        or filters["maximum-cost"]
        or len(filters["grade"])
        or len(filters["gender"])
    )


def searchOpportunities(baseQuery, search):
    if type(search) == str:
        search = search.strip()

    if not search:
        return baseQuery

    searchQueryString = "%" + search + "%"
    searchQuery = baseQuery.filter(
        or_(
            Opportunity.title.ilike(searchQueryString),
            Opportunity.description.ilike(searchQueryString),
        )
    )

    return searchQuery


def filterOpportunities(baseQuery, filtersDict):
    if not hasFilters(filtersDict):
        return baseQuery

    filters = []

    for key, val in filtersDict.items():
        subFilters = []
        if key == "field":
            for fieldFilter in val:
                subFilters.append(Opportunity.field == fieldFilter)
            filters.append(or_(*subFilters))
        elif key == "maximum-cost":
            # val is max cost filter here
            filters.append(Opportunity.cost <= val)
        elif key == "grade":
            # Restrict search space to Opportunity objects that share their ID with OpportunityGrade objects
            filters.append(Opportunity.opportunityID == OpportunityGrade.opportunityID)
            for gradeFilter in val:
                subFilters.append(OpportunityGrade.grade == gradeFilter)
            filters.append(or_(*subFilters))
        elif key == "gender":
            for genderFilter in val:
                subFilters.append(Opportunity.gender == genderFilter)
            filters.append(or_(*subFilters))

    return baseQuery.filter(and_(*filters))


def sortOpportunities(baseQuery, sort):
    sortOptionQueries = {
        "cost-asc": Opportunity.cost.asc(),
        "cost-desc": Opportunity.cost.desc(),
        "deadline-asc": Opportunity.deadline.asc(),
        "deadline-desc": Opportunity.deadline.desc(),
        "dateposted-asc": Opportunity.datePosted.asc(),
        "dateposted-desc": Opportunity.datePosted.desc(),
    }

    # default sort option
    sortOptionQuery = "dateposted-asc"

    # Check if sort is a truey value (i.e. not None or "") and is a key in sortOptionQueries
    if sort and sort in sortOptionQueries.keys():
        sortOptionQuery = sort

    sortedOpportunitiesQuery = baseQuery.order_by(sortOptionQueries[sortOptionQuery])

    return sortedOpportunitiesQuery


def findOpportunities(body):
    """
    input:
    {
        filters: {field: ["ACADEMIC PROGRAMS", "ENGINEERING, MATH, & CS", "MEDICAL & LIFE SCIENCES"], maximum-cost: 500, grade: ["JUNIOR", "SENIOR"], gender: ["CO-ED", "FEMALE"]},
        search: "query",
        sort: "sort-order"
    }
    output:
    body (provided input), array of opportunity objects
    """
    filters = body["filters"]
    search = body["search"]
    sort = body["sort"]
    baseQuery = Opportunity.query

    # Evaluate query generated by fxn compositions
    sortedOpportunities = sortOpportunities(
        filterOpportunities(searchOpportunities(baseQuery, search), filters), sort,
    ).all()

    # Attaching grades and links to the list of sorted Opportunity objects
    for opportunity in sortedOpportunities:
        grades = OpportunityGrade.query.filter_by(
            opportunityID=opportunity.opportunityID
        ).all()
        opportunity.grades = [grade.grade for grade in grades]
        links = OpportunityLink.query.filter_by(
            opportunityID=opportunity.opportunityID
        ).all()
        opportunity.links = [link.link for link in links]

    return (body, sortedOpportunities)
