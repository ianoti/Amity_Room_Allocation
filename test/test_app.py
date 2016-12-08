#! usr/bin/env
import unittest

from app import *

class TestIndividualCreation(unittest.TestCase):
    """ Initialise the Amity class """
    def setUp(self):
        self.amity = Amity()

    """ check that Amity can add rooms """
    def test_room_creation(self):
        self.amity.add_room("o", "Hogwarts")
        self.amity.add_room("l", "Narnia")
        self.assertNotEqual(0, len(self.amity.room_directory), msg='rooms did not successfully add to room_directory')
        self.assertEqual(2, len(self.amity.room_directory), msg='incorrect number of room added')
        self.assertIsInstance(self.amity.room_directory[0], Office, msg="incorrect instantiation")
        self.assertIsInstance(self.amity.room_directory[1], LivingSpace, msg="incorrect instantiation")
        self.assertListEqual([self.amity.room_directory[0].name,
            self.amity.room_directory[1].name], ["Hogwarts", "Narnia"],
            msg="room objects not properly added to room_directory")
        self.amity.add_room("office", "bigthink")
        self.assertEqual(self.amity.room_directory[2].name, "bigthink",
            msg="room option should be intuitive and flexible")

    """ check that Amity can add people individually """
    def test_add_people(self):
        self.amity.add_person("Judy", "Okatch", "staff")
        self.assertNotEqual(0, len(self.amity.waiting_list), msg="person didn't add")
        self.amity.add_person("Tom", "Bosire", "fellow")
        self.amity.add_person("Alois", "Bumbum", "fellow", "Y")
        self.assertEqual(3, len(self.amity.waiting_list), msg="adding people has failed")
        self.assertIsInstance(self.amity.waiting_list[0], Staff, msg="incorrect inheritance")
        self.assertIsInstance(self.amity.waiting_list[2], Fellow, msg="incorrect inheritance")
        self.assertEqual(self.amity.waiting_list[1].wants_living, "N", msg="default choice not loading")

class TestBatchAddition(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()

    """ check that Amity can add people from .txt file """
    def test_add_batch_people(self):
        self.amity.batch_add_person("./test_data.txt")
        self.assertNotEqual(0, len(self.amity.waiting_list), msg="didn't load people from list")
        self.assertEqual(12,len(self.amity.waiting_list,
            msg="error loading people from test_data.txt file of 12 names"))
        self.assertListEqual([self.amity.waiting_list[0].fname,
            self.amity.waiting_list[1].fname, self.amity.waiting_list[2].fname,
            self.amity.waiting_list[3].fname],
            ["OLUWAFEMI", "DOMINIC", "SIMON", "MARI"], msg="incorrect loading order or parsing")
        self.assertIsInstance(self.amity.waiting_list[7], Staff, msg="incorrect inheritance")
        self.assertListEqual([self.amity.waiting_list[4].wants_living,
            self.amity.waiting_list[5].wants_living, self.amity.waiting_list[6].wants_living],
            ["Y", "N", "Y"], msg="default values for accomodation choice incorrect")

    """ check that Amity allows for addition of multiple rooms """
    def test_multiple_room_add(self):
        self.amity.add_room("l", "Valhalla", "Narnia", "Oculus", "Octopizzo")
        self.assertEqual(4, len(self.amity.room_directory), msg="multiple room addition to be allowed")
        self.amity.add_room("o", "Kulala", "chillarea", "pambazuko")
        self.assertEqual(7, len(self.amity.room_directory), msg="multiple room"
            "addition to not overwrite directory")
        self.assertListEqual([self.amity.room_directory[0].access_allowed,
            self.amity.room_directory[4].access_allowed], [["fellow"], ["fellow", "staff"]],
            msg="multiple room addition should correctly inherit")

class TestErroneousInput(unittest.TestCase):
    """ this test will test for incorrect inputs and double additions of rooms """
    def setUp(self):
        self.amity = Amity()
        self.amity.add_room("l", "Tweepy")
        self.amity.add_person("Adrian", "Andre", "Fellow", "Y")

    """ check for preexistence of room """
    def test_room_already_exists(self):
        self.assertEqual(self.amity.add_room("l", "Tweepy"), "the room already exists",
            msg="room duplicates not allowed")
        self.assertEqual(self.amity.add_room("l", "tweepy"), "the room already exists",
            msg="room duplicates not allowed")

    """ check for wrong parameters passed to room creation """
    def test_room_add_wrong_options(self):
        self.assertListEqual([self.amity.add_room(0, "Jollyroger"),
            self.amity.add_room("o", 45)], ["the room option is invalid",
            "the room name is invalid"], msg="the arguments are invalid")
        self.assertEqual(1, len(self.amity.room_directory),
            msg="the room directory should only accept valid inputs")

    """ check for wrong parameters passed to add person """
    def test_add_person_wrong_options(self):
        self.assertListEqual([self.amity.add_person(0, "Walter", "Staff"),
            self.amity.add_person("John", "Doe", "x"), self.amity.add_person("John", 0, "fellow"),
            self.amity.add_person("John", "Doe", "Staff", "Y"),
            self.amity.add_person("John", "Doe")],
            ["the name is invalid", "the role is invalid", "the name is invalid",
            "Staff aren't eligible for accomodation", "the person's role is missing"],
            msg="the add person function should catch erroneous inputs")

        self.assertEqual(1, len(self.amity.waiting_list), msg="only add valid people")

class TestRoomAllocate(unittest.TestCase):
    """ check that room allocation is functioning """
    def setUp(self):
        self.amity = Amity()
        self.amity.add_room("o", "Valhalla", "Krypton", "Zone", "Farm", "Jericho")
        self.amity.add_room("l", "Tweepy", "Valkyrie", "Levite", "Ruby", "Bronze")
        self.amity.batch_add_person("./test_data.txt")
