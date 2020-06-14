# from datetime import datetime

# # Scholarships must be imported without prefix "app.", or else value comparisons with "==" with FAIL ("<class 'utl....ls.Scholarship'>" == "<class 'app....ls.Scholarship'>")
# from utl.database.models.models import Scholarship
# from utl.database.functions.search.searchScholarships import searchScholarships


# def test_searching_existing_scholarships(session):
#     """
#     This function uses the session fixture created in test/conftest.py
#     """
#     # arrange
#     tScholarship1 = Scholarship(title="ff", description="faf", amount=4.20, deadline=datetime.today(), eligibility="male, female")
#     tScholarship2 = Scholarship(title="gg", description="gag", amount=4.20, deadline=datetime.today(), eligibility="male, female")
#     tScholarship3 = Scholarship(title="hh", description="hah", amount=4.20, deadline=datetime.today(), eligibility="male, female")
#     session.add(tScholarship1)
#     session.add(tScholarship2)
#     session.add(tScholarship3)
#     session.commit()

#     # act
#     # searchScholarshipsScholarships1 tests getting a row in the db that exists
#     searchScholarshipsScholarships1 = searchScholarships("ff")
#     searchScholarshipsScholarships2 = searchScholarships("gag")
    
#     # assert
#     # verify that the return type of searchScholarships(query) is tuple just once
#     assert isinstance(searchScholarshipsScholarships1, tuple), "return type of searchScholarships(query) should be a tuple"
#     assert (
#         searchScholarshipsScholarships1[0] == "ff"
#     ), "0th element of returned tuple should be the query 'ff'"
#     assert(searchScholarshipsScholarships1[1] == [tScholarship1]), "should return True because only 1 scholarship matches up with a query of 'ff'"

#     assert (
#         searchScholarshipsScholarships2[0] == "gag"
#     ), "0th element of returned tuple should be the query 'gag'"
#     assert(searchScholarshipsScholarships2[1] == [tScholarship2])
   

# def test_searching_nonexistent_scholarships(session):
#     # arrange
#     # empty Scholarships table

#     # act
#     # searchScholarshipsResults tests getting a row in the db that doesn't exist
#     searchScholarshipsResults = searchScholarships("aa")

#     # assert
#     assert (
#         searchScholarshipsResults[0] == "aa"
#     ), "0th element of returned tuple should be the query 'aa'"
#     assert (
#         searchScholarshipsResults[1] == []
#     ), "1st element of returned tuple should be the result [] (no results)"


# def test_ordering_of_search_scholarships_results(session):
#     # arrange
#     tScholarship1 = Scholarship(title="ff", description="faf", amount=4.20, deadline=datetime.today(), eligibility="male, female")
#     tScholarship2 = Scholarship(title="gg", description="gag", amount=4.20, deadline=datetime.today(), eligibility="male, female")
#     tScholarship3 = Scholarship(title="hh", description="hah", amount=4.20, deadline=datetime.today(), eligibility="male, female")
#     tSearchScholarshipsResults = [tScholarship1, tScholarship2, tScholarship3]
#     session.add(tScholarship1)
#     session.add(tScholarship2)
#     session.add(tScholarship3)
#     session.commit()
    
#     searchScholarshipsResults = searchScholarships("ff")
#     sortedTSearchResults = sorted(tSearchScholarshipsResults, key=(lambda scholarship: datetime.strptime(str(scholarship.datePosted), "%Y-%m-%d %H:%M:%S.%f").date()), reverse=True)
#     assert(tSearchScholarshipsResults == sortedTSearchResults)