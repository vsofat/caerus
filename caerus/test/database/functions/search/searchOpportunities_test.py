# from datetime import datetime

# # Opportunitys must be imported without prefix "app.", or else value comparisons with "==" with FAIL ("<class 'utl....ls.Opportunity'>" == "<class 'app....ls.Opportunity'>")
# from utl.database.models.models import Opportunity
# from utl.database.functions.search.searchOpportunities import searchOpportunities


# def test_searching_existing_scholarships(session):
#     """
#     This function uses the session fixture created in test/conftest.py
#     """
#     # arrange
#     tOpportunity1 = Opportunity(title="ff", description="faf", amount=4.20, deadline=datetime.today(), eligibility="male, female")
#     tOpportunity2 = Opportunity(title="gg", description="gag", amount=4.20, deadline=datetime.today(), eligibility="male, female")
#     tOpportunity3 = Opportunity(title="hh", description="hah", amount=4.20, deadline=datetime.today(), eligibility="male, female")
#     session.add(tOpportunity1)
#     session.add(tOpportunity2)
#     session.add(tOpportunity3)
#     session.commit()

#     # act
#     # searchOpportunitiesOpportunitys1 tests getting a row in the db that exists
#     searchOpportunitiesOpportunitys1 = searchOpportunities("ff")
#     searchOpportunitiesOpportunitys2 = searchOpportunities("gag")
    
#     # assert
#     # verify that the return type of searchOpportunities(query) is tuple just once
#     assert isinstance(searchOpportunitiesOpportunitys1, tuple), "return type of searchOpportunities(query) should be a tuple"
#     assert (
#         searchOpportunitiesOpportunitys1[0] == "ff"
#     ), "0th element of returned tuple should be the query 'ff'"
#     assert(searchOpportunitiesOpportunitys1[1] == [tOpportunity1]), "should return True because only 1 scholarship matches up with a query of 'ff'"

#     assert (
#         searchOpportunitiesOpportunitys2[0] == "gag"
#     ), "0th element of returned tuple should be the query 'gag'"
#     assert(searchOpportunitiesOpportunitys2[1] == [tOpportunity2])
   

# def test_searching_nonexistent_scholarships(session):
#     # arrange
#     # empty Opportunitys table

#     # act
#     # searchOpportunitiesResults tests getting a row in the db that doesn't exist
#     searchOpportunitiesResults = searchOpportunities("aa")

#     # assert
#     assert (
#         searchOpportunitiesResults[0] == "aa"
#     ), "0th element of returned tuple should be the query 'aa'"
#     assert (
#         searchOpportunitiesResults[1] == []
#     ), "1st element of returned tuple should be the result [] (no results)"


# def test_ordering_of_search_scholarships_results(session):
#     # arrange
#     tOpportunity1 = Opportunity(title="ff", description="faf", field="", gender="", deadline=datetime.today(), eligibility="male, female")
#     tOpportunity2 = Opportunity(title="gg", description="gag", field="", gender="", deadline=datetime.today(), eligibility="male, female")
#     tOpportunity3 = Opportunity(title="hh", description="hah", field="", gender="", deadline=datetime.today(), eligibility="male, female")
#     tSearchOpportunitiesResults = [tOpportunity1, tOpportunity2, tOpportunity3]
#     session.add(tOpportunity1)
#     session.add(tOpportunity2)
#     session.add(tOpportunity3)
#     session.commit()
    
#     searchOpportunitiesResults = searchOpportunities("ff")
#     sortedTSearchResults = sorted(tSearchOpportunitiesResults, key=(lambda scholarship: datetime.strptime(str(scholarship.datePosted), "%Y-%m-%d %H:%M:%S.%f").date()), reverse=True)
#     assert(tSearchOpportunitiesResults == sortedTSearchResults)