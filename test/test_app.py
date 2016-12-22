#!/usr/bin/env python
import unittest

from app import *


class TestIndividualCreation(unittest.TestCase):
    """ Initialise the Amity class """
    def setUp(self):
        self.amity = Amity()

    """ check that Amity can add rooms """
    def test_room_creation(self):
        self.amity.add_room("o", ["Hogwarts"])
        self.amity.add_room("l", ["Narnia"])
        self.assertNotEqual(0, len(self.amity.room_directory))
        self.assertEqual(2, len(self.amity.room_directory))
        self.assertIsInstance(self.amity.room_directory[0], Office)
        self.assertIsInstance(self.amity.room_directory[1], LivingSpace)
        self.assertListEqual([self.amity.room_directory[0].name,
            self.amity.room_directory[1].name], ["hogwarts", "narnia"],
            msg="room objects not properly added to room_directory")

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

    """ check that Amity can add people from .txt file """
    def test_add_batch_people(self):
        self.amity.batch_add_person("./test_data.txt")
        self.assertNotEqual(0, len(self.amity.waiting_list))
        self.assertEqual(12,len(self.amity.waiting_list))
        self.assertListEqual([self.amity.waiting_list[0].fname,
            self.amity.waiting_list[1].fname, self.amity.waiting_list[2].fname,
            self.amity.waiting_list[3].fname],
            ["OLUWAFEMI", "DOMINIC", "SIMON", "MARI"])
        self.assertIsInstance(self.amity.waiting_list[7], Fellow)
        self.assertListEqual([self.amity.waiting_list[5].wants_living,
            self.amity.waiting_list[7].wants_living, self.amity.waiting_list[11].wants_living],
            ["Y", "N", "Y"])

    def test_add_batch_wrong_file(self):
        self.assertEqual("couldn't find file specify correct file path",self.amity.batch_add_person("re"))

    """ check that Amity allows for addition of multiple rooms """
    def test_multiple_room_add(self):
        self.amity.add_room("l", ["Valhalla", "Narnia", "Oculus", "Octopizzo"])
        self.assertEqual(4, len(self.amity.room_directory))
        self.amity.add_room("o", ["Kulala", "chillarea", "pambazuko"])
        self.assertEqual(7, len(self.amity.room_directory))
        self.assertListEqual([self.amity.room_directory[0].access_allowed,
            self.amity.room_directory[4].access_allowed], [["fellow"], ["fellow", "staff"]])


class TestErroneousInput(unittest.TestCase):
    """ this test will test for incorrect inputs and double additions of rooms """
    def setUp(self):
        self.amity = Amity()
        self.amity.add_room("l", ["Tweepy"])
        self.amity.add_person("Adrian", "Andre", "Fellow", "Y")

    """ check for preexistence of room """
    def test_room_already_exists(self):
        self.assertEqual(self.amity.add_room("l", ["Tweepy"]), "the room already exists")
        self.assertEqual(self.amity.add_room("l", ["tweepy"]), "the room already exists")

    """ check for wrong parameters passed to room creation """
    def test_room_add_wrong_options(self):
        self.assertListEqual([self.amity.add_room(0, ["Jollyroger"]),
            self.amity.add_room("o", [45])], ["the room option is invalid",
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
        self.assertEqual(len(self.amity.waiting_list),0)
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
        self.assertEqual(len(self.amity.waiting_list),7)
        self.amity.allocate()
        self.assertEqual(len(self.amity.waiting_list),1)
        self.assertEqual(len(self.amity.room_directory[0].occupants), 6)
        self.assertEqual(len(self.amity.room_directory[1].occupants), 3)

    def test_it_reallocates_successfully(self):
        self.amity.add_room("o", ["Valhalla"])
        self.amity.add_room("l", ["Tweepy"])
        self.amity.allocate()
        self.amity.add_room("o", ["Juja"])
        self.assertEqual(len(self.amity.room_directory[0].occupants), 2)
        self.assertEqual(len(self.amity.room_directory), 3)
        self.amity.reallocate(1,"Juja")
        self.assertEqual(len(self.amity.room_directory[0].occupants), 1)


class TestRetrieveDetails(unittest.TestCase):
    """ check that it retrives person id """
    def setUp(self):
        self.amity = Amity()
        self.amity.add_person("Adrian", "Andre", "Fellow", "Y")
        self.amity.add_person("Tom", "Omondi", "STAFF")

    def test_get_the_id(self):
        self.assertEqual(self.amity.get_person_id("Adrian","Andre"),"Adrian Andre has id 1")
        self.assertEqual(self.amity.get_person_id("Tom","Omondi"),"Tom Omondi has id 2")


class TestRoomPrint(unittest.TestCase):

    def setUp(self):
        self.amity = Amity()
        self.amity.add_room("o", ["Valhalla"])

    def test_nonexistant_room_print(self):
        self.assertEqual(self.amity.print_room("joom"),"the room doesn't exist")

    def test_print_for_empty_room(self):
        self.assertEqual(self.amity.print_room("valhalla"), "the room is empty")

    def test_print_room_w_occupants(self):
        self.amity.add_person("Tom","Brady","fellow")
        self.amity.allocate()
        self.assertIn("Tom Brady",self.amity.print_room("Valhalla"))


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
        self.assertEqual("There are no unallocated people nothing to output", self.amity.print_unallocated())
