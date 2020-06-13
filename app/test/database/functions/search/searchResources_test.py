import unittest

from app.__init__ import app, db as _db, create_app
from utl.database.models.models import Resource
from app.utl.database.functions.search.searchResources import searchResources


def test_search_existing_resources(session):
    """
    This function uses the session fixture created in test/conftest.py
    """
    # arrange
    tResource0 = Resource(title="ff", description="ff", link="ff")
    tResource1 = Resource(title="gg", description="gg", link="gg")
    tResource2 = Resource(title="hh", description="hh", link="hh")
    session.add(tResource0)
    session.add(tResource1)
    session.add(tResource2)
    session.commit()

    # act
    # searchedResources0 tests getting a row in the db that exists
    searchedResources0 = searchResources("ff")
    
    # assert
    assert (
        searchedResources0[0] == "ff"
    ), "0th element of returned tuple should be the query 'ff'"
    assert(searchedResources0[1] == [tResource0])
    assert(searchedResources0[1][0] == tResource0)
   

def test_search_nonexistent_resources(session):
    # arrange
    # empty Resources table

    # act
    # searchedResources1 tests getting a row in the db that doesn't exist
    searchedResources1 = searchResources("aa")

    # assert
    assert (
        searchedResources1[0] == "aa"
    ), "0th element of returned tuple should be the query 'aa'"
    assert (
        searchedResources1[1] == []
    ), "1st element of returned tuple should be the result [] (no results)"