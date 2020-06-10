from .models import db, Opportunity, OpportunityGrade, OpportunityLink
from sqlalchemy import and_, or_, in_


def findScholarships(body):
    """
    input:
    {
        search: "query",
        sort: "sort-order"
    }
    output:
    body (provided input), array of opportunity objects
    """
    search = body['search']
    sort = body['sort']

    if search == '':
        return body, sortScholarships(baseQuery, sort)
    else:
        return body, searchSortScholarships(search, sort)
