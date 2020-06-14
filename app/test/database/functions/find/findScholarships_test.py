from datetime import datetime

from utl.database.models.models import Scholarship, ScholarshipLink
from utl.database.functions.find.findScholarships import (
    findScholarships,
    sortScholarships,
    searchScholarships,
)

sortOptionQueries = {
    "dateposted-asc": Scholarship.datePosted.asc(),
    "dateposted-desc": Scholarship.datePosted.desc(),
}


def test_sortScholarships(session):
    baseQuery = Scholarship.query
    datePostedAscSortString = "dateposted-asc"
    datePostedDescSortString = "dateposted-desc"

    # arrange
    tScholarship1 = Scholarship(title="ff", description="faf", amount=4.20, deadline=datetime.today(), eligibility="male, female")
    tScholarship2 = Scholarship(title="gg", description="gag", amount=4.20, deadline=datetime.today(), eligibility="male, female")
    tScholarship3 = Scholarship(title="hh", description="hah", amount=4.20, deadline=datetime.today(), eligibility="male, female")
    tScholarshipsList = [tScholarship1, tScholarship2, tScholarship3]
    session.add(tScholarship1)
    session.add(tScholarship2)
    session.add(tScholarship3)
    session.commit()
    sortedTScholarshipsListByDatePostedAsc = sorted(
        tScholarshipsList,
        key=(
            lambda scholarship: (
                datetime.strptime(
                    str(scholarship.datePosted), "%Y-%m-%d %H:%M:%S.%f"
                ).date(),
                scholarship.scholarshipID,
            )
        ),
    )
    sortedTScholarshipsListByDatePostedDesc = sorted(
        tScholarshipsList,
        key=(
            lambda scholarship: (
                datetime.strptime(
                    str(scholarship.datePosted), "%Y-%m-%d %H:%M:%S.%f"
                ).date(),
                scholarship.scholarshipID,
            )
        ),
        reverse=True,
    )

    # act
    # dateposted-asc
    sortedScholarshipsQueryByDatePostedAsc = sortScholarships(
        baseQuery, datePostedAscSortString
    )
    sortedScholarshipsListByDatePostedAsc = sortedScholarshipsQueryByDatePostedAsc.all()
    # dateposted-desc
    sortedScholarshipsQueryByDatePostedDesc = sortScholarships(
        baseQuery, datePostedDescSortString
    )
    sortedScholarshipsListByDatePostedDesc = sortedScholarshipsQueryByDatePostedDesc.all()
    # sort was not provided or provided as None
    sortedScholarshipsQueryByDatePostedNone = sortScholarships(
        baseQuery, None
    )
    sortedScholarshipsListByDatePostedNone = sortedScholarshipsQueryByDatePostedNone.all()
    # sort was not provided or provided as ""
    sortedScholarshipsQueryByDatePostedEmptyQuotes = sortScholarships(
        baseQuery, ""
    )
    sortedScholarshipsListByDatePostedEmptyQuotes = sortedScholarshipsQueryByDatePostedNone.all()

    # assert
    for idx, scholarship in enumerate(sortedScholarshipsListByDatePostedAsc):
        assert scholarship.datePosted == sortedTScholarshipsListByDatePostedAsc[idx].datePosted

    for idx, scholarship in enumerate(sortedScholarshipsListByDatePostedDesc):
        assert scholarship.datePosted == sortedTScholarshipsListByDatePostedDesc[idx].datePosted

    for idx, scholarship in enumerate(sortedScholarshipsListByDatePostedNone):
        assert scholarship.datePosted == sortedTScholarshipsListByDatePostedAsc[idx].datePosted

    for idx, scholarship in enumerate(sortedScholarshipsListByDatePostedEmptyQuotes):
        assert scholarship.datePosted == sortedTScholarshipsListByDatePostedAsc[idx].datePosted


def test_searchScholarships(session):
    baseQuery = Scholarship.query
    search = "ff"
    datePostedAscSortString = "dateposted-asc"
    datePostedDescSortString = "dateposted-desc"

    # arrange
    tScholarship1 = Scholarship(title="ff", description="faf", amount=4.20, deadline=datetime.today(), eligibility="male, female")
    tScholarship2 = Scholarship(title="ff", description="gag", amount=4.20, deadline=datetime.today(), eligibility="male, female")
    tScholarship3 = Scholarship(title="hh", description="hah", amount=4.20, deadline=datetime.today(), eligibility="male, female")
    tScholarshipsList = [tScholarship1, tScholarship2, tScholarship3]
    session.add(tScholarship1)
    session.add(tScholarship2)
    session.add(tScholarship3)

    # act
    # Non-empty search query
    searchScholarshipsQueryNonEmpty = searchScholarships(baseQuery, search)
    searchScholarshipsResultsNonEmpty = searchScholarshipsQueryNonEmpty.all()
    # None as search query
    searchScholarshipsQueryNone = searchScholarships(baseQuery, None)
    searchScholarshipsResultsNone = searchScholarshipsQueryNone.all()
    # Empty search query
    searchScholarshipsQueryEmpty = searchScholarships(baseQuery, "")
    searchScholarshipsResultsEmpty = searchScholarshipsQueryEmpty.all()

    # assert
    # Assume that searchScholarshipsResultsNonEmpty is in no particular order because order is outside of this fxn's concern.
    # Non-empty search query
    assert isinstance(searchScholarshipsResultsNonEmpty, list)
    assert len(searchScholarshipsResultsNonEmpty) == 2
    assert tScholarship1 in searchScholarshipsResultsNonEmpty
    assert tScholarship2 in searchScholarshipsResultsNonEmpty
    # TODO: Sometimes, if the datePosted value is identical, the order of scholarship retrieval could be [<Scholarship 1>, <Scholarship 2>] or [<Scholarship 2>, <Scholarship 1>], so the check below may be faulty.
    assert searchScholarshipsResultsNonEmpty == [tScholarship1, tScholarship2]

    # None as search query
    assert isinstance(searchScholarshipsResultsNone, list)
    assert len(searchScholarshipsResultsNone) == 3
    assert tScholarship1 in searchScholarshipsResultsNone
    assert tScholarship2 in searchScholarshipsResultsNone
    assert searchScholarshipsResultsNone == [tScholarship1, tScholarship2, tScholarship3]

    # Empty search query
    assert isinstance(searchScholarshipsResultsEmpty, list)
    assert len(searchScholarshipsResultsEmpty) == 3
    assert tScholarship1 in searchScholarshipsResultsEmpty
    assert tScholarship2 in searchScholarshipsResultsEmpty
    assert searchScholarshipsResultsEmpty == [tScholarship1, tScholarship2,tScholarship3]

# TODO: Test sortScholarships(searchScholarships(..., ...), ...)

def test_findScholarships(session):
    baseQuery = Scholarship.query
    search1 = "ff"
    datePostedAscSortString = "dateposted-asc"
    datePostedDescSortString = "dateposted-desc"

    # arrange
    tScholarship1 = Scholarship(title="ff", description="faf", amount=4.20, deadline=datetime.today(), eligibility="male, female")
    tScholarship2 = Scholarship(title="ff", description="gag", amount=4.20, deadline=datetime.today(), eligibility="male, female")
    tScholarship3 = Scholarship(title="hh", description="hah", amount=4.20, deadline=datetime.today(), eligibility="male, female")
    tScholarshipsList = [tScholarship1, tScholarship2, tScholarship3]
    session.add(tScholarship1)
    session.add(tScholarship2)
    session.add(tScholarship3)
    body1 = {"search": search1, "sort": datePostedAscSortString}
    search1 = body1["search"]
    sort1 = body1["sort"]

    # Scholarship links
    tScholarshipLink1 = ScholarshipLink(scholarshipID=1, link="https:f.f")
    tScholarshipLink2 = ScholarshipLink(scholarshipID=1, link="https:g.g")
    tScholarshipLink3 = ScholarshipLink(scholarshipID=2, link="https:h.h")
    tScholarshipLink4 = ScholarshipLink(scholarshipID=2, link="https:i.i")
    tScholarshipLink5 = ScholarshipLink(scholarshipID=3, link="https:j.j")
    tScholarshipLink6 = ScholarshipLink(scholarshipID=3, link="https:k.k")

    session.add(tScholarshipLink1)
    session.add(tScholarshipLink2)
    session.add(tScholarshipLink3)
    session.add(tScholarshipLink4)
    session.add(tScholarshipLink5)
    session.add(tScholarshipLink6)
    session.commit()

    # act
    locatedScholarships1 = findScholarships(body1)
    tLocatedScholarships1 = sortScholarships(searchScholarships(baseQuery, search1), sort1).all()

    # assert
    assert locatedScholarships1 == (body1, tLocatedScholarships1)
    assert tLocatedScholarships1 == [tScholarship1, tScholarship2]
    # test links
    assert locatedScholarships1[1][0].links == ["https:f.f", "https:g.g"]
    assert locatedScholarships1[1][1].links == ["https:h.h", "https:i.i"]