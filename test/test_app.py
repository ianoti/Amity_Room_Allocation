#! usr/bin/env
import unittest

from app import *

class TestCreation(unittest.TestCase):
    """ Initialise the Amity class """

    def setUp(self):
        self.amity = Amity()

    """ check that Amity can add rooms """
    def test_room_creation(self):
        self.amity.add_room("Hogwarts", "o")
        self.amity.add_room("Narnia", "l")
        self.assertNotEqual(0, len(self.amity.room_directory), msg='rooms did not successfully add to room_directory')
        self.assertEqual(2, len(self.amity.room_directory), msg='incorrect number of room added')
        self.assertIsInstance(self.amity.room_directory[0], Office, msg="incorrect instantiation")
        self.assertIsInstance(self.amity.room_directory[1], LivingSpace, msg="incorrect instantiation")
        self.assertListEqual([self.amity.room_directory[0].name,
            self.amity.room_directory[1].name], ["Hogwarts", "Narnia"],
            msg="room objects not properly added to room_directory")
