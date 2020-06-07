from copy import deepcopy

from .models import (
    db,
    CostPreference,
    FieldPreference,
    GenderPreference,
    GradePreference,
)


# Preference Types
COST_PREFERENCE = "COST_PREFERENCE"
FIELD_PREFERENCE = "FIELD_PREFERENCE"
GENDER_PREFERENCE = "GENDER_PREFERENCE"
GRADE_PREFERENCE = "GRADE_PREFERENCE"


# Cost Preference

# Create
def createCostPreference(userID, cost):
    costPreference = CostPreference(userID=userID, cost=cost)
    db.session.add(costPreference)
    db.session.commit()


# Update
def updateCostPreference(userID, cost):  # TODO: Is this the best way to update a row?
    costPreference = CostPreference.query.filter_by(userID=userID).first()
    costPreference.cost = cost
    db.session.commit()


# Get All
def getAllCostPreferences(userID):
    costPreferences = CostPreference.query.filter_by(userID=userID).all()
    costPreferencesArr = []
    for costPreference in costPreferences:
        costPreferenceDict = {"type": COST_PREFERENCE, "value": costPreference.cost}
        costPreferencesArr.append(costPreferenceDict)
    return costPreferencesArr


# Field Preference

# Create
def createFieldPreference(userID, field):
    fieldPreference = FieldPreference(userID=userID, field=field)
    db.session.add(fieldPreference)
    db.session.commit()


# Get All
def getAllFieldPreferences(userID):
    fieldPreferences = FieldPreference.query.filter_by(userID=userID).all()
    fieldPreferencesArr = []
    for fieldPreference in fieldPreferences:
        fieldPreferenceDict = {"type": FIELD_PREFERENCE, "value": fieldPreference.field}
        fieldPreferencesArr.append(fieldPreferenceDict)
    return fieldPreferencesArr


# Gender Preference

# Create
def createGenderPreference(userID, gender):
    genderPreference = GenderPreference(userID=userID, gender=gender)
    db.session.add(genderPreference)
    db.session.commit()


# Get All
def getAllGenderPreferences(userID):
    genderPreferences = GenderPreference.query.filter_by(userID=userID).all()
    genderPreferencesArr = []
    for genderPreference in genderPreferences:
        genderPreferenceDict = {
            "type": GENDER_PREFERENCE,
            "value": genderPreference.gender,
        }
        genderPreferencesArr.append(genderPreferenceDict)
    return genderPreferencesArr


# Grade Preference

# Create
def createGradePreference(userID, grade):
    gradePreference = GradePreference(userID=userID, grade=grade)
    db.session.add(gradePreference)
    db.session.commit()


# Get All
def getAllGradePreferences(userID):
    GradePreferences = FieldPreference.query.filter_by(userID=userID).all()
    GradePreferencesArr = []
    for gradePreference in GradePreferences:
        gradePreferenceDict = {"type": GRADE_PREFERENCE, "value": gradePreference.grade}
        GradePreferencesArr.append(gradePreferenceDict)
    return GradePreferencesArr


def createPreference(userID, preferenceType, preferenceValue):
    """
    Match the given preferenceType with the corresponding create functions for that preference type.

    For cost preferences, there can only be one row for a given userID. Thus, we can update that one row every time.
    First, we determine if that preference record already exists in the corresponding table with the given userID.
    Then, if it already exists, update the row with new values. If it doesn't exist, create a new row with the given
    values.
    """
    if preferenceType == COST_PREFERENCE:
        # TODO: Is this the most optimal way to check for existence?
        if CostPreference.query.filter_by(userID=userID).first():
            updateCostPreference(userID, preferenceValue)
        else:
            createCostPreference(userID, preferenceValue)
    elif preferenceType == FIELD_PREFERENCE:
        createFieldPreference(userID, preferenceValue)
    elif preferenceType == GENDER_PREFERENCE:
        createGenderPreference(userID, preferenceValue)
    elif preferenceType == GRADE_PREFERENCE:
        createGradePreference(userID, preferenceValue)


def createAllPreferences(body):
    """
    Input
    -----
    An array of preference dictionaries, each with its own type and value.
    For example, the dictionary representation of a cost preference with a 
    value of 500 is {type: "COST_PREFERENCE", value: 500}. Another example
    would be a gender preference with a value of female, whose dictionary 
    representation would be {type: "GENDER_PREFERENCE", value: "FEMALE"}.
    If a user wants both of these preferences, this function will receive
    [{type: "COST_PREFERENCE", value: 500}, {type: "GENDER_PREFERENCE", 
    value: "FEMALE"}].
    """
    userID = body.userID

    # Delete one to many rows in field, gender, and grade tables with a given userID, so that updated rows can be created
    # Since we have a different updating mechanism for CostPreference, it is taken care of in the createPreference function.
    FieldPreference.query.filter_by(userID=userID).delete()
    GenderPreference.query.filter_by(userID=userID).delete()
    GradePreference.query.filter_by(userID=userID).delete()

    # Create a preference for each of the given preferences
    for preference in body.preferences:
        createPreference(userID, preference.type, preference.value)


def getAllPreferences(userID):
    """
    Output
    -----
    An array of preference dictionaries, each with its own type and value.
    See the createAllPreferences function for an example.
    """
    costPreferences = deepcopy(getAllCostPreferences(userID))
    fieldPreferences = deepcopy(getAllFieldPreferences(userID))
    genderPreferences = deepcopy(getAllGenderPreferences(userID))
    gradePreferences = deepcopy(getAllGradePreferences(userID))

    allPreferences = (
        costPreferences + fieldPreferences + genderPreferences + gradePreferences
    )
    return allPreferences
