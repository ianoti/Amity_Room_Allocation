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

    """ method to add people to system utilising models"""
    @staticmethod
    def add_person(fname, sname, role, wants_living = "N"):
        pass

    """ method to add rooms to system utilising models specified"""
    @staticmethod
    def add_room(rm_name, rm_type):
        rm_variable = rm_name.lower()
        if rm_type == "o":
            rm_variable = Office(rm_name)
            pass #after creation using Office class append to room_directory
        elif rm_type == "l":
            rm_variable = LivingSpace(rm_name)
            pass #after creation using LivingSpace class append to room_directory
        else:
            print ("the option given to create room is invalid")

    """  method to load names from txt file """
    @staticmethod
    def load_persons():
        """ load some text from file and pass as argument to create person """
        pass

    """ method to create rooms and append to a list """
    @staticmethod
    def add_person(fname, sname, role="none", wants_living="N"):
        pass
