from .models import db, User


def createUser(userID, email, name, imglink, userType, accessToken, refreshToken):
    user = User(
        userID=userID,
        email=email,
        name=name,
        imglink=imglink,
        userType=userType,
        accessToken=accessToken,
        refreshToken=refreshToken
    )
    db.session.add(user)
    db.session.commit()


def nullifyTokens(userID):
    user = User.query.filter_by(userID=userID).first()
    user.accessToken = None
    user.refreshToken = None
    db.session.commit()


def getTokens(userID):
    user = User.query.filter_by(userID=userID).first()
    return user.accessToken, user.accessToken
