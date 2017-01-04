#!/usr/bin/env python
import unittest
import os

from app import *


class TestIndividualCreation(unittest.TestCase):
    """ Initialise the Amity class """
    def setUp(self):
        self.amity = Amity()

    """ check that Amity can add rooms """
    def test_room_creation(self):
        self.amity.add_room("o", ["Hogwarts"])
        self.amity.add_room("l", ["Narnia"])
        self.assertEqual(2, len(self.amity.room_directory))
        self.assertIsInstance(self.amity.room_directory[0], Office)
        self.assertIsInstance(self.amity.room_directory[1], LivingSpace)
        self.assertListEqual([self.amity.room_directory[0].name,
                              self.amity.room_directory[1].name],
                             ["hogwarts", "narnia"])

    """ check that Amity can add people individually """
    def test_add_people(self):
        self.amity.add_person("Judy", "Okatch", "staff")
        self.assertNotEqual(0, len(self.amity.waiting_list))
        self.amity.add_person("Tom", "Bosire", "fellow")
        self.amity.add_person("Alois", "Bumbum", "fellow", "Y")
        self.assertEqual(3, len(self.amity.waiting_list))
        self.assertIsInstance(self.amity.waiting_list[0], Staff)
        self.assertIsInstance(self.amity.waiting_list[2], Fellow)
        self.assertEqual(self.amity.waiting_list[1].wants_living, "N")


class TestBatchAddition(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()
        self.tst_frmt = "file tests that system checks formatting"
        self.tst = "OLUWAFEMI SULE FELLOW Y\nDOMINIC WALTERS STAFF\n"
        self.tst += "SIMON PATTERSON FELLOW Y\nMARI LAWRENCE FELLOW Y\n"
        self.tst += "LEIGH RILEY STAFF\nTANA LOPEZ FELLOW Y\n"
        self.tst += "KELLY McGUIRE STAFF\nJOHN DOE FELLOW N\n"
        self.tst += "ELIZABETH WARREN STAFF\nJANE DOE FELLOW Y\n"
        self.tst += "ANSLEM OKUMU STAFF\nJULIAN PRINCE FELLOW Y\n"
        test_file = open("sample_test.txt", "w")
        test_file.write(self.tst)
        test_file.close()
        test_file = open("sample_test_format.txt", "w")
        test_file.write(self.tst_frmt)
        test_file.close()

    """ check that Amity can add people from .txt file """
    def test_add_batch_people(self):
        self.amity.batch_add_person("sample_test.txt")
        self.assertNotEqual(0, len(self.amity.waiting_list))
        self.assertEqual(12, len(self.amity.waiting_list))
        self.assertListEqual([self.amity.waiting_list[0].fname,
                              self.amity.waiting_list[1].fname,
                              self.amity.waiting_list[2].fname,
                              self.amity.waiting_list[3].fname],
                             ["OLUWAFEMI", "DOMINIC", "SIMON", "MARI"])
        self.assertIsInstance(self.amity.waiting_list[7], Fellow)
        self.assertListEqual([self.amity.waiting_list[5].wants_living,
                              self.amity.waiting_list[7].wants_living,
                              self.amity.waiting_list[11].wants_living],
                             ["Y", "N", "Y"])

    """ test that Amity doesn't crash if wrong file path specified"""
    def test_add_batch_wrong_file(self):
        self.assertEqual("couldn't find file specify correct file path",
                         self.amity.batch_add_person("re"))
        self.assertEqual(len(self.amity.waiting_list), 0)

    """ test that Amity handles incorrectly formatted text files"""
    def test_add_batch_wrong_file_formatting(self):
        self.assertEqual("the text file has formatting errors",
                         self.amity.batch_add_person("sample_test_format.txt"))
        self.assertEqual(len(self.amity.waiting_list), 0)

    """ check that Amity allows for addition of multiple rooms """
    def test_multiple_room_add(self):
        self.amity.add_room("l", ["Valhalla", "Narnia", "Oculus", "Octopizzo"])
        self.assertEqual(4, len(self.amity.room_directory))
        self.amity.add_room("o", ["Kulala", "chillarea", "pambazuko"])
        self.assertEqual(7, len(self.amity.room_directory))
        self.assertListEqual([self.amity.room_directory[0].access_allowed,
                              self.amity.room_directory[4].access_allowed],
                             [["fellow"], ["fellow", "staff"]])

    @classmethod
    def tearDownClass(cls):
        os.remove("sample_test.txt")
        os.remove("sample_test_format.txt")


class TestErroneousInput(unittest.TestCase):
    """ this test will test for incorrect inputs and double
    additions of rooms """
    def setUp(self):
        self.amity = Amity()
        self.amity.add_room("l", ["Tweepy"])
        self.amity.add_person("Adrian", "Andre", "Fellow", "Y")

    """ check for preexistence of room """
    def test_room_already_exists(self):
        self.assertEqual(self.amity.add_room("l", ["Tweepy"]),
                         "the room already exists")
        self.assertEqual(self.amity.add_room("l",
                         ["tweepy"]), "the room already exists")

    """ check for wrong parameters passed to room creation """
    def test_room_add_wrong_options(self):
        self.assertListEqual([self.amity.add_room(0, ["Jollyroger"]),
                              self.amity.add_room("o", [45])],
                             ["the room option is invalid",
                              "the room name is invalid"])
        self.assertEqual(1, len(self.amity.room_directory))


class TestRoomAllocate(unittest.TestCase):
    """ check that room allocation is functioning """
    def setUp(self):
        self.amity = Amity()
        self.amity.add_person("Adrian", "Andre", "Fellow", "Y")
        self.amity.add_person("Tom", "Omondi", "STAFF")

    def test_simple_allocation(self):
        self.amity.add_room("o", ["Valhalla"])
        self.amity.add_room("l", ["Tweepy"])
        self.amity.allocate()
        self.assertEqual(len(self.amity.waiting_list), 0)
        self.assertEqual(len(self.amity.room_directory[0].occupants), 2)
        self.assertEqual(len(self.amity.room_directory[1].occupants), 1)

    def test_it_leaves_unallocated_in_waiting_list(self):
        self.amity.add_room("o", ["Valhalla"])
        self.amity.add_room("l", ["Tweepy"])
        self.amity.add_person("Tom", "Bobby", "STAFF")
        self.amity.add_person("Hope", "Lucy", "Fellow", "Y")
        self.amity.add_person("Tom", "Brady", "Fellow", "Y")
        self.amity.add_person("Joan", "juja", "staff")
        self.amity.add_person("Koech", "Tom", "staff")
        self.assertEqual(len(self.amity.waiting_list), 1)
        self.assertEqual(len(self.amity.room_directory[0].occupants), 6)
        self.assertEqual(len(self.amity.room_directory[1].occupants), 3)

    def test_it_reallocates_successfully(self):
        self.amity.add_room("o", ["Valhalla"])
        self.amity.add_room("l", ["Tweepy"])
        self.amity.allocate()
        self.amity.add_room("o", ["Juja"])
        self.assertEqual(len(self.amity.room_directory[0].occupants), 2)
        self.assertEqual(len(self.amity.room_directory), 3)
        self.amity.reallocate(1, "Juja")
        self.assertEqual(len(self.amity.room_directory[0].occupants), 1)


class TestRetrieveDetails(unittest.TestCase):
    """ check that it retrives person id """
    def setUp(self):
        self.amity = Amity()
        self.amity.add_person("Adrian", "Andre", "Fellow", "Y")
        self.amity.add_person("Tom", "Omondi", "STAFF")

    def test_get_the_id(self):
        self.assertEqual(self.amity.get_person_id("Adrian", "Andre"),
                         "Adrian Andre fellow has id 1\n")
        self.assertEqual(self.amity.get_person_id("Tom", "Omondi"),
                         "Tom Omondi staff has id 2\n")


class TestRoomPrint(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()
        self.amity.add_room("o", ["Valhalla"])

    def test_nonexistant_room_print(self):
        self.assertEqual(self.amity.print_room("joom"),
                         "the room doesn't exist")

    def test_print_for_empty_room(self):
        self.assertEqual(self.amity.print_room("valhalla"),
                         "the room is empty")

    def test_print_room_w_occupants(self):
        self.amity.add_person("Tom", "Brady", "fellow")
        self.amity.allocate()
        self.assertIn("Tom Brady", self.amity.print_room("Valhalla"))


class TestUnallocatedPrint(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()
        self.amity.add_person("Tom", "Brady", "Fellow")
        self.amity.add_person("Anderson", "John", "staff")

    def test_unallocated_people_print(self):
        self.assertIn("Anderson John", self.amity.print_unallocated())

    def test_unallocated_print_if_all_allocated(self):
        self.amity.add_room("o", ["Hogwarts"])
        self.amity.allocate()
        self.assertEqual("There are no unallocated people nothing to output",
                         self.amity.print_unallocated())
