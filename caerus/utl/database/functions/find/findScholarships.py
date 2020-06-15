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

    # default sort option
    sortOptionQuery = "dateposted-asc"

    # Check if sort is a truey value (i.e. not None or "") and is a key in sortOptionQueries
    if sort and sort in sortOptionQueries.keys():
        sortOptionQuery = sort

    sortedScholarshipsQuery = baseQuery.order_by(sortOptionQueries[sortOptionQuery])

    return sortedScholarshipsQuery


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
        locatedScholarships = sortScholarships(searchScholarships(baseQuery, search), sort).all()

    for scholarship in locatedScholarships:
        links = ScholarshipLink.query.filter_by(
            scholarshipID=scholarship.scholarshipID
        ).all()
        scholarship.links = [link.link for link in links]

    return body, locatedScholarships