import unittest
from __init__ import app


class Test(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        self.app = app.test_client()


if __name__ == "__main__":
    unittest.main()

