#! usr/bin/env
import unittest

from app import Amity

class TestSessionInitialisation(unittest.TestCase):
    def test_session_start(self):
        session = Amity()
        self.assertIsInstance(session, Amity, msg = "failed to initialise Amity")
