from utl.database.models.models import db, User


def createUser(userID, email, name, imglink, userType, accessToken, refreshToken):
    user = User(
        userID=userID,
        email=email,
        name=name,
        imglink=imglink,
        userType=userType,
        accessToken=accessToken,
        refreshToken=refreshToken,
    )
    db.session.add(user)
    db.session.commit()


def userExists(userID):
    return db.session.query(User.query.filter(User.userID == userID).exists()).scalar()


def nullifyTokens(userID):
    user = User.query.filter_by(userID=userID).first()
    user.accessToken = None
    user.refreshToken = None
    db.session.commit()


def getTokens(userID):
    user = User.query.filter_by(userID=userID).first()
    return user.accessToken, user.accessToken


def updateTokens(userID, access, refresh):
    user = User.query.filter_by(userID=userID).first()
    user.accessToken = access
    user.refreshToken = refresh
    db.session.commit()


def getUserInfo(userID):
    user = User.query.filter_by(userID=userID).first()
    return user


def getAllUsersInfo():
    return User.query.all()

