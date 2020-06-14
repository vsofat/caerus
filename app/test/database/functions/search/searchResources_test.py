# from datetime import datetime

# # Resources must be imported without prefix "app.", or else value comparisons with "==" with FAIL ("<class 'utl....ls.Resource'>" == "<class 'app....ls.Resource'>")
# from utl.database.models.models import Resource
# from utl.database.functions.search.searchResources import searchResources


# def test_searching_existing_resources(session):
#     """
#     This function uses the session fixture created in test/conftest.py
#     """
#     # arrange
#     tResource1 = Resource(title="ff", description="faf", link="fif")
#     tResource2 = Resource(title="gg", description="gag", link="gig")
#     tResource3 = Resource(title="hh", description="hah", link="hih")
#     session.add(tResource1)
#     session.add(tResource2)
#     session.add(tResource3)
#     session.commit()

#     # act
#     # searchResourcesResults1 tests getting a row in the db that exists
#     searchResourcesResults1 = searchResources("ff")
#     searchResourcesResults2 = searchResources("faf")

#     # assert
#     # verify that the return type of searchResources(query) is tuple just once
#     assert isinstance(
#         searchResourcesResults1, tuple
#     ), "return type of searchResources(query) should be a tuple"
#     assert (
#         searchResourcesResults1[0] == "ff"
#     ), "0th element of returned tuple should be the query 'ff'"
#     assert searchResourcesResults1[1] == [
#         tResource1
#     ], "should return True because only 1 resource matches up with a query of 'ff'"

#     assert (
#         searchResourcesResults2[0] == "faf"
#     ), "0th element of returned tuple should be the query 'faf'"
#     assert searchResourcesResults2[1] == [tResource1]


# def test_searching_nonexistent_resources(session):
#     # arrange
#     # empty Resources table

#     # act
#     # searchResourcesResults tests getting a row in the db that doesn't exist
#     searchResourcesResults = searchResources("aa")

#     # assert
#     assert (
#         searchResourcesResults[0] == "aa"
#     ), "0th element of returned tuple should be the query 'aa'"
#     assert (
#         searchResourcesResults[1] == []
#     ), "1st element of returned tuple should be the result [] (no results)"


# def test_ordering_of_search_resources_results(session):
#     # arrange
#     tResource1 = Resource(title="ff", description="faf", link="fif")
#     tResource2 = Resource(title="ff", description="gag", link="gig")
#     tResource3 = Resource(title="ff", description="hah", link="hih")
#     tSearchResourcesResults = [tResource1, tResource2, tResource3]
#     session.add(tResource1)
#     session.add(tResource2)
#     session.add(tResource3)
#     session.commit()

#     searchResourcesResults = searchResources("ff")
#     sortedTSearchResults = sorted(
#         tSearchResourcesResults,
#         key=(
#             lambda resource: datetime.strptime(
#                 str(resource.datePosted), "%Y-%m-%d %H:%M:%S.%f"
#             ).date()
#         ),
#         reverse=True,
#     )
#     assert tSearchResourcesResults == sortedTSearchResults
