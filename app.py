#!/usr/bin/env python
import os
import random
"""
    This module implements Amity as a class based interface for the entire
    room allocation system
"""

from models.person import Fellow, Staff
from models.room import Office, LivingSpace

class Amity(object):

    def __init__(self):
        self.room_directory = []
        self.waiting_list = []

    def add_person(self, fname, sname, role="none", wants_living = "N"):
        """ method to add people to system utilising models"""
        if isinstance(fname, str) and isinstance(sname, str):
            if role.lower() == "fellow":
                person = Fellow(fname, sname, role, wants_living)
            elif role.lower() == "staff":
                if wants_living == "Y":
                    return "Staff aren't eligible for accomodation"
                else:
                    person = Staff(fname, sname)
            else:
                return "the role is invalid"
            self.waiting_list.append(person)
        elif not isinstance(fname, str) or not isinstance(sname, str):
            return "the name is invalid"

    def add_room(self, rm_type, *given_names):
        """ method to add rooms to system utilising models specified """
        for rm_name in given_names:
            if isinstance(rm_type, str) and isinstance(rm_name, str):
                rm_variable =  rm_name.lower()
                if rm_variable not in [room.name for room in self.room_directory]:
                    if rm_type == "l":
                        room = LivingSpace(rm_variable)
                    elif rm_type == "o" or "office":
                        room = Office(rm_variable)
                    else:
                        print ("the option given to create room is invalid")
                    self.room_directory.append(room)
                else:
                    return "the room already exists"
            elif not isinstance(rm_type, str):
                return "the room option is invalid"
            elif not isinstance(rm_name, str):
                return "the room name is invalid"

    def available_rooms(self):
        for room in

    def allocate(self):
        for person in self.waiting_list:
            

    def reallocate(self, fname, sname, new_rm):
        """ method to allow for reallocation of users between rooms """
        pass

    def batch_add_person(self, file_path):
        """  method to load names from txt file and add people to system """
        with open(file_path, "r") as people_file:
            for person_string in people_file:
                person_details = person_string.rstrip().split()
                if len(person_details) == 4:
                    self.add_person(person_details[0], person_details[1], person_details[2], person_details[3])
                elif len(person_details) == 3:
                    self.add_person(person_details[0], person_details[1], person_details[2])
                else:
                    return "the text file has formatting errors"

    def print_room_occupants(self, rm_name):
        """ print the occupants in a room given the room name """

    @staticmethod
    def save_system_state():
        """ method to save state to database """
        pass

    @staticmethod
    def load_system_state():
        """ method to load state from database """
        pass

c = Amity()
c.add_person("Judy", "Okatch", "staff")
# c.add_room("o", "Hogwarts")
print(c.room_directory)
print(c.waiting_list)

c.allocate()
