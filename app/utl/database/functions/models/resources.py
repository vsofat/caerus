from utl.database.models.models import db, Resource


def getAllResources():
    resources = Resource.query.order_by(Resource.datePosted.desc()).all()
    return resources


def getResource(resourceID):
    resource = Resource.query.filter_by(resourceID=resourceID).first()
    return resource


def createResource(body):
    resource = Resource(
        title=body['title'], description=body['description'], link=body['link'])
    db.session.add(resource)
    db.session.commit()


def deleteResource(resourceID):
    Resource.query.filter_by(resourceID=resourceID).delete()
    db.session.commit()
