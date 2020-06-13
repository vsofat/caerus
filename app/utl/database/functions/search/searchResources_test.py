import unittest

from caerus import *
from ....database.models.models import db, Resource
from utl.database.functions.search.searchResources import searchResources
from ........app.__init__ import app


class TestSearchResources(unittest.TestCase):
    def setUp(self):
        db.init_app("sqlite://")
        db.Model.create_all()

        tResource0 = Resource(title="ff", description="ff", link="ff")
        tResource1 = Resource(title="gg", description="gg", link="gg")
        tResource1 = Resource(title="hh", description="hh", link="hh")
        db.session.add(tResource0)
        db.session.add(tResource1)
        db.commit()

    def test_searching_resources(self):
        resources = searchResources("gg")
        assert resources is not None

    def tearDown(self):
        db.drop_all()


if __name__ == "__main__":
    unittest.main()
