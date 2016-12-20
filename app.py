#!/usr/bin/env python
import os
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

    """ method to add people to system utilising models"""
    @staticmethod
    def add_person(fname, sname, role="none", wants_living = "N"):
        pass

    """ method to add rooms to system utilising models specified.
        the add room method should be able to accept multiple
        inputs
    """

    def add_room(self, rm_type, *given_names):
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

    """  method to load names from txt file """

    @staticmethod
    def batch_add_person(file_path):
        """ load some text from file and pass as argument to create person """
        pass


    """ method to save state to database """
    @staticmethod
    def save_system_state():
        pass

    """ method to load state from database """
    @staticmethod
    def load_system_state():
        pass

    """ method that will be called to allocate rooms to fellows and staff """
    @staticmethod
    def allocate():
        pass

    """ method that will reallocate people based on the unique emp_id """
