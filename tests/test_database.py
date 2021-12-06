import unittest
from unittest.mock import Mock

# pylint: disable=import-error
# from app.api.database import get_user

class DatabseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.user = Mock()
        self.user.configure_mock(id="435423796234072", firstname="John", lastname="Doe")

    def test_can_connect(self):
        pass

    def test_get_user(self):
        pass


if __name__ == "__main__":
    unittest.main()