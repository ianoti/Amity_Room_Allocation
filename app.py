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
        self.people_directory = []
        self.living_waiting_list = []

    def add_person(self, fname, sname, role="none", wants_living = "N"):
        """ method to add people to system utilising models"""
        if isinstance(fname, str) and isinstance(sname, str):
            if role.lower() == "fellow":
                person = Fellow(fname, sname, role, wants_living)
                person.p_id = int(len(self.people_directory)+1)
            elif role.lower() == "staff":
                if wants_living == "Y":
                    return "Staff aren't eligible for accomodation"
                else:
                    person = Staff(fname, sname)
                    person.p_id = int(len(self.people_directory)+1)
            else:
                return "the role is invalid"
            self.waiting_list.append(person)
            self.people_directory.append(person)
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

    def get_rooms_w_people(self):
        """ filter room directory to return rooms with occupants"""
        rooms_w_people = [room for room in self.room_directory
            if len(room.occupants)>=1]
        return rooms_w_people

    def get_person_id(self, fsname, ssname):
        """ search the person id given names """
        search = [person for person in self.people_directory
            if person.fname.lower()==fsname.lower() and person.sname.lower()==ssname.lower()]
        if len(search) == 0:
            print("no records found")
        if len(search) >= 1:
            for person in search:
                print("{} {} has id {}".format(person.fname,person.sname,person.p_id))

    def allocate(self):
        """ assign people to rooms """
        #make a copy of waiting list to allow remove() method to run bug free
        iteration_list = [guys for guys in self.waiting_list]
        for person in iteration_list:
            available_office = self.get_available_space("o")
            available_living = self.get_available_space("l")
            if len(available_office)==0 and len(available_living)==0:
                return "No rooms are available"

            if (person.role == "staff" or
                (person.role == "fellow" and person.wants_living.lower() == "n")):
                if len(available_office)>= 1:
                    allocated_office = random.choice(available_office)
                    allocated_office.occupants.append(person)
                    self.waiting_list.remove(person)
                else:
                    return "Offices have filled"

            if (person.role == "fellow" and person.wants_living.lower() == "y"):
                if len(available_office)>= 1 and len(available_living)>=1:
                    allocated_office = random.choice(available_office)
                    allocated_office.occupants.append(person)
                    allocated_living = random.choice(available_living)
                    allocated_living.occupants.append(person)
                    self.waiting_list.remove(person)
                elif len(available_office)>= 1 and len(available_living)==0:
                    allocated_office = random.choice(available_office)
                    allocated_office.occupants.append(person)
                    self.waiting_list.remove(person)
                    self.living_waiting_list.append(person)
                    return "Can't allocate Living Space"

    def reallocate(self, person_id, room_name):
        """ method to allow for reallocation of users between rooms """
        occupied_room = self.get_rooms_w_people()
        print(len(occupied_room))
        #person_id is used to retrieve person object used in comprehension
        person_retr = [person for person in self.people_directory if person.p_id == person_id]
        if len(person_retr):
            move_person = person_retr[0]
            #check if the person is in a room to remove from
            old_room = [room for room in occupied_room if move_person in room.occupants]
            if len(old_room):
                #use comprehension to return destination room if it exists
                new_room = [room for room in self.room_directory if room.name.lower()==room_name.lower()]
                if len(new_room):
                    old_room[0].occupants.remove(move_person)
                    new_room[0].occupants.append(move_person)
                else:
                    return "The room doesn't exist"
            else:
                return "the person isn't in a room run allocate to assign them to rooms"
        else:
            return "That person id doesn't have a user"




    def print_unallocated(self, option = "no"):
        """display a list of unallocated people on screen optional writing to file"""
        if option == "no":
            if len(self.waiting_list)>=1:
                print("People who have yet to be allocated")
                print("#"*50)
                for person in self.waiting_list:
                    if isinstance(person, Fellow):
                        print("Name: {} {} Role: {} Wants accomodation:{}"
                            .format(person.fname, person.sname, person.role, person.wants_living))
                    elif isinstance(person, Staff):
                        print("Name: {} {} Role: {}".format(person.fname,person.sname, person.role))
            elif len(self.waiting_list)==0:
                print("all people have been allocated")

        elif option == "-o":
            file = open("./data/unallocated_people.txt", "w")
            if len(self.waiting_list)>=1:
                file.write("People who have yet to be allocated\n")
                file.write("#"*50+"\n")
                for person in self.waiting_list:
                    if isinstance(person, Fellow):
                        file.write("Name: {} {} Role: {} Wants accomodation:{}\n"
                            .format(person.fname, person.sname, person.role, person.wants_living))
                    elif isinstance(person, Staff):
                        file.write("Name: {} {} Role: {}\n".format(person.fname,person.sname, person.role))
            else:
                file.write("There are no unallocated people")
            file.close()

    def print_allocations(self, option = "no"):
        """ print out people currently allocated to a room and the room name """
        rooms_w_guys = self.get_rooms_w_people()
        if option == "no":
            if len(rooms_w_guys) == 0:
                print("No people have been allocated yet")
            elif len(rooms_w_guys) >= 1:
                print("People allocated to room and room name")
                for room in rooms_w_guys:
                    print("{}".format(room.name))
                    print("-"*50)
                    member_string = ""
                    for person in room.occupants:
                        member_string += ("{} {} {} ,".format(person.fname, person.sname, person.role))
                    print (member_string)

        elif option == "-o":
            file = open("./data/allocated_people.txt", "w")
            if len(rooms_w_guys) >=1:
                file.write("People allocated to room and room name\n")
                for room in rooms_w_guys:
                    file.write("{}\n".format(room.name))
                    file.write("-"*50+"\n")
                    member_string = ""
                    for person in room.occupants:
                        member_string += ("{} {} {} ,".format(person.fname, person.sname, person.role))
                    file.write(member_string+"\n")
            else:
                file.write("No people have been allocated yet")
            file.close()



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

    def print_room(self, rm_name):
        """ print the occupants in a room given the room name """
        room_exists = [room for room in self.room_directory if room.name.lower() == rm_name.lower()]
        if len(room_exists):
            for room in room_exists:
                members=""
                if len(room.occupants)>=1:
                    for person in room.occupants:
                        members += (" {} {},".format(person.fname, person.sname))
                    print (members)
                else:
                    print("The room is empty")
        else:
            print("the room doesn't exist")

    def save_system_state():
        """ method to save state to database """
        pass

    @staticmethod
    def load_system_state():
        """ method to load state from database """
        pass


c = Amity()
c.batch_add_person("./test/test_data.txt")
c.add_room("o", "Kulala", "chillarea", "pambazuko")
c.add_room("l", "tweepy", "pick", "popo")
c.allocate()
c.print_allocations("-o")
