from datetime import datetime

from utl.database.models.models import Resource
from utl.database.functions.find.findResources import (
    findResources,
    sortResources,
    searchResources,
)

sortOptionQueries = {
    "dateposted-asc": Resource.datePosted.asc(),
    "dateposted-desc": Resource.datePosted.desc(),
}


def test_sortResources(session):
    baseQuery = Resource.query
    datePostedAscSortString = "dateposted-asc"
    datePostedDescSortString = "dateposted-desc"

    # arrange
    tResource1 = Resource(title="ff", description="faf", link="fif")
    tResource2 = Resource(title="gg", description="gag", link="gig")
    tResource3 = Resource(title="hh", description="hah", link="hih")
    tResourcesList = [tResource1, tResource2, tResource3]
    session.add(tResource1)
    session.add(tResource2)
    session.add(tResource3)
    session.commit()
    sortedTResourcesListByDatePostedAsc = sorted(
        tResourcesList,
        key=(
            lambda resource: (
                datetime.strptime(
                    str(resource.datePosted), "%Y-%m-%d %H:%M:%S.%f"
                ).date(),
                resource.resourceID,
            )
        ),
    )
    sortedTResourcesListByDatePostedDesc = sorted(
        tResourcesList,
        key=(
            lambda resource: (
                datetime.strptime(
                    str(resource.datePosted), "%Y-%m-%d %H:%M:%S.%f"
                ).date(),
                resource.resourceID,
            )
        ),
        reverse=True,
    )

    # act
    # dateposted-asc
    sortedResourcesQueryByDatePostedAsc = sortResources(
        baseQuery, datePostedAscSortString
    )
    sortedResourcesListByDatePostedAsc = sortedResourcesQueryByDatePostedAsc.all()
    # dateposted-desc
    sortedResourcesQueryByDatePostedDesc = sortResources(
        baseQuery, datePostedDescSortString
    )
    sortedResourcesListByDatePostedDesc = sortedResourcesQueryByDatePostedDesc.all()
    # sort was not provided or provided as None
    sortedResourcesQueryByDatePostedNone = sortResources(
        baseQuery, None
    )
    sortedResourcesListByDatePostedNone = sortedResourcesQueryByDatePostedNone.all()
    # sort was not provided or provided as ""
    sortedResourcesQueryByDatePostedEmptyQuotes = sortResources(
        baseQuery, ""
    )
    sortedResourcesListByDatePostedEmptyQuotes = sortedResourcesQueryByDatePostedNone.all()

    # assert
    for idx, resource in enumerate(sortedResourcesListByDatePostedAsc):
        assert resource.datePosted == sortedTResourcesListByDatePostedAsc[idx].datePosted

    for idx, resource in enumerate(sortedResourcesListByDatePostedDesc):
        assert resource.datePosted == sortedTResourcesListByDatePostedDesc[idx].datePosted

    for idx, resource in enumerate(sortedResourcesListByDatePostedNone):
        assert resource.datePosted == sortedTResourcesListByDatePostedAsc[idx].datePosted

    for idx, resource in enumerate(sortedResourcesListByDatePostedEmptyQuotes):
        assert resource.datePosted == sortedTResourcesListByDatePostedAsc[idx].datePosted


def test_searchResources(session):
    baseQuery = Resource.query
    search = "ff"
    datePostedAscSortString = "dateposted-asc"
    datePostedDescSortString = "dateposted-desc"

    # arrange
    tResource1 = Resource(title="ff", description="faf", link="fif")
    tResource2 = Resource(title="ff", description="gag", link="gig")
    tResource3 = Resource(title="hh", description="hah", link="hih")
    tResourcesList = [tResource1, tResource2, tResource3]
    session.add(tResource1)
    session.add(tResource2)
    session.add(tResource3)

    # act
    # Non-empty search query
    searchResourcesQueryNonEmpty = searchResources(baseQuery, search)
    searchResourcesResultsNonEmpty = searchResourcesQueryNonEmpty.all()
    # None as search query
    searchResourcesQueryNone = searchResources(baseQuery, None)
    searchResourcesResultsNone = searchResourcesQueryNone.all()
    # Empty search query
    searchResourcesQueryEmpty = searchResources(baseQuery, "")
    searchResourcesResultsEmpty = searchResourcesQueryEmpty.all()

    # assert
    # Assume that searchResourcesResultsNonEmpty is in no particular order because order is outside of this fxn's concern.
    # Non-empty search query
    assert isinstance(searchResourcesResultsNonEmpty, list)
    assert len(searchResourcesResultsNonEmpty) == 2
    assert tResource1 in searchResourcesResultsNonEmpty
    assert tResource2 in searchResourcesResultsNonEmpty
    # TODO: Sometimes, if the datePosted value is identical, the order of resource retrieval could be [<Resource 1>, <Resource 2>] or [<Resource 2>, <Resource 1>], so the check below may be faulty.
    assert searchResourcesResultsNonEmpty == [tResource1, tResource2]

    # None as search query
    assert isinstance(searchResourcesResultsNone, list)
    assert len(searchResourcesResultsNone) == 3
    assert tResource1 in searchResourcesResultsNone
    assert tResource2 in searchResourcesResultsNone
    assert searchResourcesResultsNone == [tResource1, tResource2, tResource3]

    # Empty search query
    assert isinstance(searchResourcesResultsEmpty, list)
    assert len(searchResourcesResultsEmpty) == 3
    assert tResource1 in searchResourcesResultsEmpty
    assert tResource2 in searchResourcesResultsEmpty
    assert searchResourcesResultsEmpty == [tResource1, tResource2,tResource3]

# TODO: Test sortResources(searchResources(..., ...), ...)

def test_findResources(session):
    baseQuery = Resource.query
    search1 = "ff"
    datePostedAscSortString = "dateposted-asc"
    datePostedDescSortString = "dateposted-desc"

    # arrange
    tResource1 = Resource(title="ff", description="faf", link="fif")
    tResource2 = Resource(title="ff", description="gag", link="gig")
    tResource3 = Resource(title="hh", description="hah", link="hih")
    tResourcesList = [tResource1, tResource2, tResource3]
    session.add(tResource1)
    session.add(tResource2)
    session.add(tResource3)
    body1 = {"search": search1, "sort": datePostedAscSortString}
    search1 = body1["search"]
    sort1 = body1["sort"]

    # act
    locatedResources1 = findResources(body1)
    tLocatedResources1 = sortResources(searchResources(baseQuery, search1), sort1).all()

    # assert
    assert locatedResources1 == (body1, tLocatedResources1)
    assert tLocatedResources1 == [tResource1, tResource2]