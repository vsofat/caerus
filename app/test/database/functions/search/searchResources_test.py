import pytest

from app.__init__ import app, db
from app.utl.database.models.models import *


@pytest.fixture
def setUp():
    db_uri = "sqlite:///:memory:"
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQL_ALCHEMY_DATABASE_URI"] = db_uri
    appTestClient = app.test_client()
    db.create_all(appTestClient)

@pytest.fixture
def tearDown():
    db.session.remove()
    db.drop_all()

def test_db_connection():
    setUp
    db.session.commit()
