from .models import db, Opportunity


def filterOpportunities(selectedFilters):
    """
    Parameters
    ----------
    query:
    filters: a dictionary of filter type to filter values, where the filter types are: field, maximum price, grade, and gender
    ex: {field: ["ACADEMIC PROGRAMS", "ENGINEERING, MATH, & CS", "MEDICAL & LIFE SCIENCES"], maximumPrice: 500, grade: [
    "JUNIOR", "SENIOR"], gender: ["CO-ED", "FEMALE"]}
    """

    # Filters array to store a list of filter conditionals to apply onto a given list of opportunities
    filters = []

    # Pull out relevant fields in the selectedFilters dictionary for later use
    selectedFieldFilters = selectedFilters['field']
    selectedMaximumPriceFilter = selectedFilters['maximumPrice']
    selectedGradeFilters = selectedFilters['grade']
    selectedGenderFilters = selectedFilters['gender']

    # For now, apply filters on a list of opportunities from the entire Opportunities db table
    opportunities = Opportunity.query

    # Dynamically append field filters to the filters array
    for selectedFieldFilter in selectedFieldFilters:
        filters.append(getattr(Opportunity, field) == selectedFieldFilter)

    # Dynamically append maximum price filter to the filters array
    filters.append(getattr(Opportunity, cost) <= selectedMaximumPriceFilter)

    # Dynamically append grade filters to the filters array
    for selectedGradeFilter in selectedGradeFilters:
        filters.append(getattr(Opportunity, grade) == selectedGradeFilter)

    # Dynamically append gender filters to the filters array
    for selectedGenderFilter in selectedGradeFilters:
        filters.append(getattr(Opportunity, gender) == selectedGenderFilter)

    # Finally, apply the filters array onto the given list of opportunities
    filteredOpportunities = opportunities.filter(*filters).all()

    return filteredOpportunities


sort():
    model.query.sort_by().all()
sortsearch():
    model.query.filter(model.title.like(search)).sort_by().all()
filtersort():

filtersortsearch():

if filters.len == 0:
    if search == '':
        sort()
    sortsearch()
if search == '':
    filtersort()
filtersortsearch()

search -> filter -> sort
