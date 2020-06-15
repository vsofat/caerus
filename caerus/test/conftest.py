import os
import pytest
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

from __init__ import app, db as _db, create_app


class TestConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    WTF_CSRF_ENABLED = False


@pytest.fixture(scope="session")
def app(request):
    """
    Returns session-wide application.
    """
    return create_app(TestConfig)


@pytest.fixture(scope="function")
def db(app, request):
    """
    Returns session-wide initialised database.
    """
    _db.init_app(app)
    with app.app_context():
        _db.drop_all()
        _db.create_all()


@pytest.fixture(scope="function", autouse=True)
def session(app, db, request):
    """
    Returns function-scoped session.
    """
    with app.app_context():
        conn = _db.engine.connect()
        txn = conn.begin()

        options = dict(bind=conn, binds={})
        sess = _db.create_scoped_session(options=options)

        # establish  a SAVEPOINT just before beginning the test
        # (http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#using-savepoint)
        sess.begin_nested()

        @event.listens_for(sess(), "after_transaction_end")
        def restart_savepoint(sess2, trans):
            # Detecting whether this is indeed the nested transaction of the test
            if trans.nested and not trans._parent.nested:
                # The test should have normally called session.commit(),
                # but to be safe we explicitly expire the session
                sess2.expire_all()
                sess.begin_nested()

        _db.session = sess
        yield sess

        # Cleanup
        sess.remove()
        # This instruction rollsback any commit that were executed in the tests.
        txn.rollback()
        conn.close()


# Credits:
# https://github.com/pytest-dev/pytest-flask/issues/70#issuecomment-361005780
# http://alexmic.net/flask-sqlalchemy-pytest/
