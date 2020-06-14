from utl.database.models.models import db, Scholarship, ScholarshipLink
from sqlalchemy import or_


def sortScholarships(baseQuery, sort):
    sortOptionQueries = {
        "amount-asc": Scholarship.amount.asc(),
        "amount-desc": Scholarship.amount.desc(),
        "deadline-asc": Scholarship.deadline.asc(),
        "deadline-desc": Scholarship.deadline.desc(),
        "dateposted-asc": Scholarship.datePosted.asc(),
        "dateposted-desc": Scholarship.datePosted.desc(),
    }

    sortedScholarships = baseQuery.order_by(sortOptionQueries[sort]).all()

    for scholarship in sortedScholarships:
        links = ScholarshipLink.query.filter_by(
            scholarshipID=scholarship.scholarshipID
        ).all()
        scholarship.links = [link.link for link in links]

    return sortedScholarships


def searchScholarships(baseQuery, search):
    # If search is None or ""
    if not search:
        return Scholarship.query

    search = search.strip()
    searchQueryString = "%" + search + "%"
    searchQuery = Scholarship.query.filter(
        or_(Scholarship.title.ilike(searchQueryString), Scholarship.description.ilike(searchQueryString))
    )
    return searchQuery


def findScholarships(body):
    """
    input:
    {
        search: "query",
        sort: "sort-order"
    }
    output:
    body (provided input), array of scholarship objects
    """
    search = body["search"]
    sort = body["sort"]
    locatedScholarships = None
    baseQuery = Scholarship.query

    if search == "":
        locatedScholarships = sortScholarships(baseQuery, sort).all()
    else:
        locatedScholarships = sortScholarships(searchScholarships(baseQuery), sort).all()

    return body, locatedScholarships