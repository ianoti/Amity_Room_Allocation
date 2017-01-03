#!/usr/bin/env python
"""
This module performs the testing for the database functionality
in the system
"""

import os
import unittest
from app import *


class TestDatabaseCreationTest(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()
        self.amity_ins1 = Amity()
        self.amity_ins2 = Amity()
        self.amity.add_room("o", ["Hogwarts", "Tweepy", "Juja"])
        self.amity.add_room("l", ["Occulus", "Jolly", "Tricky"])
        self.amity.add_person("Adrian", "Andre", "Fellow", "Y")
        self.amity.add_person("Tom", "Omondi", "STAFF")

    def test_check_save_database_works(self):
        output = self.amity.save_system_state("temporary.db")
        self.assertEqual("The data has been stored "
                         "in the database: temporary.db", output)

    def test_check_successfully_loading(self):
        expected = self.amity_ins1.load_system_state("temporary.db")
        self.assertEqual("The system state has been restored "
                         "from: temporary.db", expected)
        self.assertEqual(len(self.amity_ins1.room_directory), 6)

    def test_it_handles_undefined_databases(self):
        expected = self.amity.load_system_state("foo.wrongname")
        self.assertEqual("there was a problem with database: foo.wrongname"
                         " please confirm the database name is correct",
                         expected)
        self.assertEqual(0, len(self.amity_ins2.room_directory))

    @classmethod
    def tearDownClass(cls):
        os.remove("temporary.db")
