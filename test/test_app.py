#! usr/bin/env
import unittest
import sys

sys.path.append("../")

from app import Amity

class TestSessionInitialisation(unittest.TestCase):
    def test_session_start(self):
        session = Amity()
        self.assertIsInstance(session, Amity, msg = "failed to initialise Amity")
