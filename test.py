#! usr/bin/env
import unittest
import sys

sys.path.append("../models")

from models.person import Fellow, Staff

class TestAttributeSetting(unittest.TestCase):

    def test_person_attribute(self):
        john = Fellow("John", "Doe", "Fellow", "Y")
        njush = Fellow("Myman", "hallo", "Fellow")
        jane = Staff("Jane", "Wewe")
        self.assertIsInstance(john, Fellow, msg="Failed to create a new Fellow")
        self.assertIsInstance(jane, Staff, msg="Failed to create a new Staff")
        self.assertListEqual(["fellow", "staff"], [john.role, jane.role],
            msg="incorrect attribute settings")
        self.assertEqual(njush.wants_living, "N", msg = "error inheriting")
