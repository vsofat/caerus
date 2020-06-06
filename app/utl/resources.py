from .models import db, Resource


def getAllResources():
    resources = Resource.query.all().order_by(Resource.datePosted.desc())
    return resources


def getResource(resourceID):
    resource = Resource.query.filter_by(resourceID=resourceID).first()
    return resource


def createResource(body):
    resource = Resource(
        title=body.title, description=body.description, link=body.link)
    db.session.add(resource)
    db.session.commit()
