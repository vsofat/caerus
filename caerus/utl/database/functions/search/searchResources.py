from utl.database.models.models import db, Resource


def searchResources(query):
    like = "%" + query + "%"
    resources = (
        Resource.query.filter(
            (Resource.title.like(like)) | (Resource.description.like(like))
        )
        .order_by(Resource.datePosted.desc())
        .all()
    )
    return query, resources
