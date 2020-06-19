import unittest
import datetime

from __init__ import app


class Test(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        self.app = app.test_client()

    def test_home(self):
        return self.app.get('/', follow_redirects=True)


if __name__ == "__main__":
    unittest.main()
