#! #! usr/bin/env
"""
    This module implements Amity as a class based interface for the entire
    room allocation system
"""

from models.person import Fellow, Staff
from models.room import Office, LivingSpace


class Amity(object):
    def __init__(self):
        self.person_list = []
        self.room_directory = []
    """
        This method will use the Fellow and Staff models to create instances of
        fellow and staff and append it to a list of people
    """
    @staticmethod
    def add_person(fname, sname, role, wants_living = "N"):
        # if role == "fellow":
        #     fellow = Fellow(self, fname, sname, role, wants_living = "N")
        #     self.person_list.append(fellow)
        #     for person in self.person_list:
        #         print (person.fna)
    """
        This method will use the Room and LivingSpace models to create instances of
        LivingSpace and Office and append it to a list of rooms
    """
    @staticmethod
    def add_room(name, type):
        if type == "o":
            pass #after creation using Office class append to room_directory
        elif type == "l":
            pass #after creation using LivingSpace class append to room_directory
        else:
            print ("the option given to create room is invalid")
