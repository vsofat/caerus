from utl.database.models.models import db, Resource
from sqlalchemy import or_


def sortResources(baseQuery, sort):
    sortOptionQueries = {
        "dateposted-asc": Resource.datePosted.asc(),
        "dateposted-desc": Resource.datePosted.desc(),
    }

    # default sort option
    sortOptionQuery = "dateposted-asc"

    # Check if sort is a truey value (i.e. not None or "") and is a key in sortOptionQueries
    if sort and sort in sortOptionQueries.keys():
        sortOptionQuery = sort

    sortedResources = baseQuery.order_by(sortOptionQueries[sortOptionQuery])

    return sortedResources


def searchResources(baseQuery, search):
    # If search is None or ""
    if not search:
        return Resource.query

    search = search.strip()
    searchQueryString = "%" + search + "%"
    
    searchQuery = baseQuery.filter(
        or_(Resource.title.ilike(searchQueryString), Resource.description.ilike(searchQueryString))
    )

    return searchQuery


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
    locatedResources = None
    baseQuery = Resource.query

    if search == "":
        locatedResources = sortResources(baseQuery, sort).all()
    else:
        locatedResources = sortResources(searchResources(baseQuery, search), sort).all()

    return body, locatedResources
