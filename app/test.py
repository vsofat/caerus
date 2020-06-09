import unittest
from __init__ import app


class Test(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        self.app = app.test_client()

    def test_home(self):
        print("GET request to / route")
        return self.app.get('/', follow_redirects=True)

    def test_logout(self):
        print("GET request to /logout route")
        return self.app.get('/logout', follow_redirects=True)

    def test_opportunities(self):
        print("GET request to /opportunities route")
        return self.app.get('/opportunities', follow_redirects=True)


if __name__ == "__main__":
    unittest.main()
