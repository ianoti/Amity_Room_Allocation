#! usr/bin/env
import unittest

from models.person import Fellow, Staff
from models.room import Office, LivingSpace

class TestPersonAttribute(unittest.TestCase):

    def test_person_attribute(self):
        john = Fellow("John", "Doe", "Fellow", "Y")
        njush = Fellow("Myman", "hallo", "Fellow")
        jane = Staff("Jane", "Wewe")
        self.assertIsInstance(john, Fellow, msg="Failed to create a new Fellow")
        self.assertIsInstance(jane, Staff, msg="Failed to create a new Staff")
        self.assertListEqual(["fellow", "staff"], [john.role, jane.role],
            msg="incorrect attribute settings")
        self.assertListEqual([njush.wants_living, john.wants_living],
            ["N", "Y"], msg = "error inheriting")

class TestRoomAttribute(unittest.TestCase):

    def test_room_attribute(self):
        narnia = Office("Narnia")
        tweet = LivingSpace("Zone")
        self.assertIsInstance(narnia, Office, msg = "couldn't create Office instance")
        self.assertIsInstance(tweet, LivingSpace, msg = "couldn't create LivingSpace instance")
        self.assertListEqual([["fellow"],["fellow", "staff"]], [tweet.access_allowed, narnia.access_allowed]
            , msg = "incorrect access level")
        self.assertListEqual([4, 6], [tweet.capacity, narnia.capacity], msg ="error in capacity")
        self.assertListEqual([0, 0], [len(narnia.occupants),len(tweet.occupants)], msg ="error in occupancy")
