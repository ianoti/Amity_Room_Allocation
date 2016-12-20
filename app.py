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
        self.living_waiting_list = []

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
                    new_room = [room]
                    self.room_directory.extend(new_room)
                else:
                    return "the room already exists"
            elif not isinstance(rm_type, str):
                return "the room option is invalid"
            elif not isinstance(rm_name, str):
                return "the room name is invalid"

    def get_available_space(self, room_type):
        """ filter the room directory to return available rooms for occupancy """
        if room_type == "o":
            office_w_space = [room for room in self.room_directory
                if (len(room.occupants)< room.capacity) and isinstance(room, Office)]
            return office_w_space
        elif room_type == "l":
            living_w_space = [room for room in self.room_directory
                if (len(room.occupants)< room.capacity) and isinstance(room, LivingSpace)]
            return living_w_space

    def allocate(self):
        """ assign people to rooms """
        available_office = self.get_available_space("o")
        available_living = self.get_available_space("l")
        #make a copy of waiting list to allow remove() method to run bug free
        iteration_list = [guys for guys in self.waiting_list]
        if len(available_office) == 0 and len(available_living) == 0:
            print("Can't allocate no Rooms available")
        elif len(available_office) >= 1:
            for person in iteration_list:
                if person.role == "staff":
                    allocated_office = random.choice(available_office)
                    allocated_office.occupants.append(person)
                    for guy in allocated_office.occupants:
                        print (guy.fname)
                    self.waiting_list.remove(person)
                elif person.role == "fellow" and person.wants_living.lower() == "n":
                    allocated_office = random.choice(available_office)
                    allocated_office.occupants.append(person)
                    self.waiting_list.remove(person)
                elif person.role == "fellow" and person.wants_living.lower() == "y":
                    if len(available_living) >= 1:
                        allocated_office = random.choice(available_office)
                        allocated_living = random.choice(available_living)
                        allocated_living.occupants.append(person)
                        allocated_office.occupants.append(person)
                        self.waiting_list.remove(person)
                    else:
                        self.living_waiting_list.append(person)
                        return "Can't allocate Living Space"

    def reallocate(self, fname, sname, new_rm):
        """ method to allow for reallocation of users between rooms """
        pass

    def print_unallocated(self):
        """ this will display a list of unallocated people on screen optional writing to file"""
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
c.add_room("o", "Valhalla")
c.add_room("l", "Tweepy")
c.add_person("Tom", "Omondi", "STAFF")
c.add_person("Bob", "Omondi", "STAFF")
c.add_person("Jerry", "Omondi", "STAFF")
c.add_person("RImothy", "Omondi", "STAFF")
c.add_person("blake", "Omondi", "STAFF")
print("initial waiting list", len(c.waiting_list))
c.allocate()
print("final length", len(c.waiting_list))
