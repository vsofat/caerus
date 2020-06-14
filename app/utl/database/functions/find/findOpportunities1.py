from utl.database.models.models import db, Opportunity, OpportunityGrade, OpportunityLink
from sqlalchemy import and_, or_


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

    if not hasFilters(filters):
        if search == "":
            baseQuery = Opportunity.query
            return body, sortOpportunities(baseQuery, sort)
        else:
            return body, searchSortOpportunities(search, sort)
    elif search == "":
        return body, filterSortOpportunities(baseQuery, filters, sort)
    else:
        return body, searchFilterSortOpportunities(search, filters, sort)


def sortOpportunities(baseQuery, sort):
    sortOptionQueries = {
        "cost-asc": Opportunity.cost.asc(),
        "cost-desc": Opportunity.cost.desc(),
        "deadline-asc": Opportunity.deadline.asc(),
        "deadline-desc": Opportunity.deadline.desc(),
        "dateposted-asc": Opportunity.datePosted.asc(),
        "dateposted-desc": Opportunity.datePosted.desc(),
    }

    sortedOpportunities = baseQuery.order_by(sortOptionQueries[sort]).all()

    for opportunity in sortedOpportunities:
        grades = OpportunityGrade.query.filter_by(
            opportunityID=opportunity.opportunityID
        ).all()
        opportunity.grades = [grade.grade for grade in grades]
        links = OpportunityLink.query.filter_by(
            opportunityID=opportunity.opportunityID
        ).all()
        opportunity.links = [link.link for link in links]

    return sortedOpportunities


def searchSortOpportunities(search, sort):
    like = "%" + search + "%"
    searchQuery = Opportunity.query.filter(
        or_(Opportunity.title.like(like), Opportunity.description.like(like))
    )
    return sortOpportunities(searchQuery, sort)


# pythonic way
def filterSortOpportunities(baseQuery, filters, sort):
    fieldFilters = filters["field"]
    maximumCostFilter = filters["maximum-cost"]
    gradeFilters = filters["grade"]
    genderFilters = filters["gender"]

    opportunities = baseQuery.all()
    filteredOpportunities = []

    if len(fieldFilters) == 0:
        fieldFilters = ["Academic Programs", "Business & Jobs", "Community Service", "Govt & Law", "Leadership & Advocacy", "Museums & Art",
                        "Parks, Zoos, & Nature", "Engineering, Math, & CS", "Medical & Life Sciences", "Literature", "Performing Arts", "Visual Arts"]

    if maximumCostFilter == None:
        maximumCostFilter = 100000

    if len(gradeFilters == 0):
        gradeFilters = ["9", "10", "11", "12"]

    if len(genderFilters) == 0:
        genderFilters = ["CO-ED", "MALE", "FEMALE"]

    for opportunity in opportunities:
        if (
            opportunity.field in fieldFilters
            and opportunity.cost < maximumCostFilter
            and opportunity.gender in genderFilters
        ):
            if len(gradeFilters) == 0:
                filteredOpportunities.append(opportunity)
            else:
                OpportunityGrades = OpportunityGrade.query.filter_by(
                    opportunityID=opportunity.opportunityID
                ).all()
                grades = [grade.grade for grade in OpportunityGrades]
                for gradeFilter in gradeFilters:
                    if gradeFilter in grades:
                        filteredOpportunities.append(opportunity)
                        break

    ids = [
        filteredOpportunity.opportunityID
        for filteredOpportunity in filteredOpportunities
    ]
    filterQuery = Opportunity.filter(Opportunity.opportunityID.in_(ids))
    return sortOpportunities(filterQuery, sort)


# sql way 1


def filterSortOpportunities2(baseQuery, filters, sort):
    fieldFilters = filters["field"]
    maximumCostFilter = filters["maximum-cost"]
    gradeFilters = filters["grade"]
    genderFilters = filters["gender"]

    if len(fieldFilters) == 0:
        fieldFilters = ["Academic Programs", "Business & Jobs", "Community Service", "Govt & Law", "Leadership & Advocacy", "Museums & Art",
                        "Parks, Zoos, & Nature", "Engineering, Math, & CS", "Medical & Life Sciences", "Literature", "Performing Arts", "Visual Arts"]

    if maximumCostFilter == None:
        maximumCostFilter = 100000

    if len(gradeFilters == 0):
        gradeFilters = ["9", "10", "11", "12"]

    if len(genderFilters) == 0:
        genderFilters = ["CO-ED", "MALE", "FEMALE"]

    IDQuery = baseQuery.with_entities(Opportunity.opportunityID).filter(
        and_(
            Opportunity.field.in_(fieldFilters),
            Opportunity.cost <= maximumCostFilter,
            Opportunity.gender.in_(genderFilters),
        )
    )

    opportunityIDs = [opportunity[0] for opportunity in IDQuery]

    filteredIDQuery = OpportunityGrade.query.with_entities(
        OpportunityGrade.opportunityID
    ).filter(
        and_(
            OpportunityGrade.opportunityID.in_(opportunityIDs),
            OpportunityGrade.grade.in_(gradeFilters),
        )
    )
    filteredOpportunityIDs = [opportunity[0]
                              for opportunity in filteredIDQuery]

    finalQuery = Opportunity.query.filter(
        Opportunity.opportunityID.in_(filteredOpportunityIDs)
    )

    return sortOpportunities(finalQuery, sort)


# sql way 2


def filterSortOpportunities3(baseQuery, filters, sort):
    fieldFilters = filters["field"]
    maximumCostFilter = filters["maximum-cost"]
    gradeFilters = filters["grade"]
    genderFilters = filters["gender"]

    if len(fieldFilters) == 0:
        fieldFilters = ["Academic Programs", "Business & Jobs", "Community Service", "Govt & Law", "Leadership & Advocacy", "Museums & Art",
                        "Parks, Zoos, & Nature", "Engineering, Math, & CS", "Medical & Life Sciences", "Literature", "Performing Arts", "Visual Arts"]

    if maximumCostFilter == None:
        maximumCostFilter = 100000

    if len(gradeFilters == 0):
        gradeFilters = ["9", "10", "11", "12"]

    if len(genderFilters) == 0:
        genderFilters = ["CO-ED", "MALE", "FEMALE"]

    FirstQuery = baseQuery.filter(
        and_(
            Opportunity.field.in_(fieldFilters),
            Opportunity.cost <= maximumCostFilter,
            Opportunity.gender.in_(genderFilters),
        )
    )

    filteredIDQuery = OpportunityGrade.query.with_entities(
        OpportunityGrade.opportunityID
    ).filter(OpportunityGrade.grade.in_(gradeFilters))
    filteredOpportunityIDs = [opportunity[0]
                              for opportunity in filteredIDQuery]

    SecondQuery = Opportunity.query.filter(
        Opportunity.opportunityID.in_(filteredOpportunityIDs)
    )

    finalQuery = FirstQuery.intersect(SecondQuery)

    return sortOpportunities(finalQuery, sort)


def searchFilterSortOpportunities(search, filters, sort):
    like = "%" + search + "%"
    searchQuery = Opportunity.query.filter(
        or_(Opportunity.title.like(like), Opportunity.description.like(like))
    )
    return filterSortOpportunities(searchQuery, filters, sort)


def hasFilters(filters):
    """
    input:
    {field: ["ACADEMIC PROGRAMS", "ENGINEERING, MATH, & CS", "MEDICAL & LIFE SCIENCES"],
        maximum-cost: 500, grade: ["JUNIOR", "SENIOR"], gender: ["CO-ED", "FEMALE"]}
    output:
    True or False
    """
    return not (
        len(filters["field"]) == 0
        and filters["maximum-cost"] == None
        and len(filters["grade"]) == 0
        and len(filters["gender"]) == 0
    )
