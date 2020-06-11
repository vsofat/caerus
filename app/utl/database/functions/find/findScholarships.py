from ..models import db, Scholarship, ScholarshipLink
from sqlalchemy import or_


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

    if search == "":
        baseQuery = Scholarship.query
        return body, sortScholarships(baseQuery, sort)
    else:
        return body, searchSortScholarships(search, sort)


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


def searchSortScholarships(search, sort):
    like = "%" + search + "%"
    searchQuery = Scholarship.query.filter(
        or_(Scholarship.title.like(like), Scholarship.description.like(like))
    )
    return sortScholarships(searchQuery, sort)
