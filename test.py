#! usr/bin/env
import unittest
import sys.path
from person import Fellow, Staff

class TestClassExistance(unittest.TestCase):

    def test_fellow_attribute(self):
        john = Fellow("John Doe")
        jane = Staff("Jane Doe")
        self.assertIsInstance(john, Fellow, msg="Failed to create a new Fellow")
        self.assertIsInstance(jane, Staff, msg="Failed to create a new Staff")
        self.assertListEqual(["fellow", "staff"], [john.access, jane.access],
            msg="wrong access level")
        self.assertListEqual(["unallocated", "unallocated"], [john.location, jane.location],
            msg="the person has been erroniously allocated")
