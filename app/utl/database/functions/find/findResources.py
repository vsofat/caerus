from utl.database.models.models import db, Resource
from sqlalchemy import or_


def findResources(body):
    """
    input:
    {
        search: "query",
        sort: "sort-order"
    }
    output:
    body (provided input), array of resource objects
    """
    search = body["search"]
    sort = body["sort"]

    if search == "":
        baseQuery = Resource.query
        return body, sortResources(baseQuery, sort)
    else:
        return body, searchResources(sortResources(baseQuery, sort), search)


def sortResources(baseQuery, sort):
    sortOptionQueries = {
        "dateposted-asc": Resource.datePosted.asc(),
        "dateposted-desc": Resource.datePosted.desc(),
    }
    sortedResources = baseQuery.order_by(sortOptionQueries[sort])

    return sortedResources


def searchResources(baseQuery, search):
    like = "%" + search + "%"
    searchQuery = Resource.query.filter(
        or_(Resource.title.like(like), Resource.description.like(like))
    )
    return searchQuery
