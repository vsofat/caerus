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

    # assert
    for idx, resource in enumerate(sortedResourcesListByDatePostedAsc):
        assert resource.datePosted == sortedTResourcesListByDatePostedAsc[idx].datePosted

    for idx, resource in enumerate(sortedResourcesListByDatePostedDesc):
        assert resource.datePosted == sortedTResourcesListByDatePostedDesc[idx].datePosted


def test_searchResources(session):
    assert True
