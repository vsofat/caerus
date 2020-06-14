import unittest
import datetime

from __init__ import app


class Test(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        self.app = app.test_client()

    def test_home(self):
        return self.app.get('/', follow_redirects=True)

    def test_logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_opportunities(self):
        return self.app.get('/opportunities', follow_redirects=True)

    def test_opp_post(self):
        req = self.app.post('/opportunities/create', data={
            'title': 'Title',
            'description': 'Description',
            'field': 'Field',
            'gender': 'Female',
            'location': 'New York',
            'startDate': datetime.datetime.now(),
            'endDate': datetime.datetime.now(),
            'deadline': datetime.datetime.now(),
            'cost': 100,
            'grades': '9,10,11,12',
            'link0': 'google.com',
            'link1': 'bing.com'
        })
        self.assertEqual(req.status_code, 302)


if __name__ == "__main__":
    unittest.main()
