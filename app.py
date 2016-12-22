#!/usr/bin/env python
"""
    This module implements Amity as a class based interface for the entire
    room allocation system
"""
import random
import pickle
import sqlite3

from models.person import Fellow, Staff
from models.room import Office, LivingSpace


class Amity(object):

    def __init__(self):
        self.room_directory = []
        self.waiting_list = []
        self.people_directory = []
        self.living_waiting_list = []

    def add_person(self, fname, sname, role="none", wants_living="N"):
        """ method to add people to system utilising models"""
        if isinstance(fname, str) and isinstance(sname, str):
            if role.lower() == "fellow":
                person = Fellow(fname, sname, role, wants_living)
                person.p_id = int(len(self.people_directory)+1)
                self.waiting_list.append(person)
                self.people_directory.append(person)
                return("fellow added")
            elif role.lower() == "staff":
                if wants_living == "Y":
                    return "Staff aren't eligible for accomodation"
                else:
                    person = Staff(fname, sname)
                    person.p_id = int(len(self.people_directory)+1)
                    self.waiting_list.append(person)
                    self.people_directory.append(person)
                    return("staff added")
            else:
                return "the role is invalid:must be staff or fellow"

        else:
            return "the name is invalid"

    def add_room(self, rm_type, given_names):
        """ method to add rooms to system utilising models specified """
        if type(rm_type) is not str:
            return "the room option is invalid"
        for room_names in given_names:
            if type(room_names) is not str:
                return "the room name is invalid"
            else:
                rm_variable = room_names.lower()
                if rm_variable in [room.name for room in self.room_directory]:
                    return "the room already exists"
                else:
                    if rm_type == "l":
                        room = LivingSpace(rm_variable)
                        self.room_directory.append(room)
                        print("successfully added living space")
                    elif rm_type == "o":
                        room = Office(rm_variable)
                        self.room_directory.append(room)
                        print("successfully added office")
                    else:
                        print("the option given to create room is invalid",
                              "use: o or l")

    def get_available_space(self, room_type):
        """
        filter the room directory to return
        available rooms for occupancy
        """
        if room_type == "o":
            office_w_space = [room for room in self.room_directory
                              if (len(room.occupants) < room.capacity)
                              and isinstance(room, Office)]
            return office_w_space
        elif room_type == "l":
            living_w_space = [room for room in self.room_directory
                              if (len(room.occupants) < room.capacity)
                              and isinstance(room, LivingSpace)]
            return living_w_space

    def get_rooms_w_people(self):
        """ filter room directory to return rooms with occupants"""
        rooms_w_people = [room for room in self.room_directory
                          if len(room.occupants) >= 1]
        return rooms_w_people

    def get_person_id(self, fsname, ssname):
        """ search the person id given names """
        search = [person for person in self.people_directory
                  if person.fname.lower() == fsname.lower()
                  and person.sname.lower() == ssname.lower()]
        if len(search) == 0:
            return "no records found"
        if len(search) >= 1:
            for person in search:
                return("{} {} has id {}".format(person.fname, person.sname,
                                                person.p_id))

    def allocate(self):
        """ assign people to rooms """
        # make a copy of waiting list to allow remove() method to run bug free
        iteration_list = [guys for guys in self.waiting_list]
        for person in iteration_list:
            available_office = self.get_available_space("o")
            available_living = self.get_available_space("l")
            if len(available_office) == 0 and len(available_living) == 0:
                return "Couldn't allocate, no rooms available"

            if (person.role == "staff" or (person.role == "fellow" and
               person.wants_living.lower() == "n")):
                if len(available_office) >= 1:
                    allocated_office = random.choice(available_office)
                    allocated_office.occupants.append(person)
                    self.waiting_list.remove(person)
                else:
                    return "The offices are filled"

            if (person.role == "fellow" and
               person.wants_living.lower() == "y"):
                if len(available_office) >= 1 and len(available_living) >= 1:
                    allocated_office = random.choice(available_office)
                    allocated_office.occupants.append(person)
                    allocated_living = random.choice(available_living)
                    allocated_living.occupants.append(person)
                    self.waiting_list.remove(person)
                elif len(available_office) >= 1 and len(available_living) == 0:
                    allocated_office = random.choice(available_office)
                    allocated_office.occupants.append(person)
                    self.waiting_list.remove(person)
                    self.living_waiting_list.append(person)
                    return ("Can't allocate Living Space person moved"
                            "to waiting list")

    def reallocate(self, person_id, room_name):
        """ method to allow for reallocation of users between rooms """
        occupied_room = self.get_rooms_w_people()
        # person_id is used to retrieve person object used in comprehension
        print(len(self.people_directory))
        person_retr = [person for person in self.people_directory
                       if person.p_id == person_id]
        if len(person_retr) >= 1:
            move_person = person_retr[0]
            # check if the person is in a room to remove from
            old_room = [room for room in occupied_room
                        if move_person in room.occupants]
            if len(old_room) >= 1:
                # use comprehension to return destination room if it exists
                new_room = [room for room in self.room_directory
                            if room.name.lower() == room_name.lower()]
                if len(new_room):
                    original_room = [roomold for roomold in old_room
                                     if roomold.type == new_room[0].type]
                    if len(original_room):
                        original_room[0].occupants.remove(move_person)
                        new_room[0].occupants.append(move_person)
                    else:
                        print("the room types for allocation must be equal")
                else:
                    print("The room doesn't exist confirm name of room")
            else:
                print("the person isn't in a room."
                      "wait for automatic assignement")
        else:
            print("The user couldn't be found")

    def print_unallocated(self, option=None):
        """
        display a list of unallocated people on
        screen optional writing to file
        """
        if len(self.waiting_list) >= 1:
            print_str = "\nPeople who have yet to be allocated\n" + "#"*50
            print_str += ("\n" + "-"*5 + "Name" + "-"*10 +
                          "Role" + "-"*5 + "Accomodation")
            for person in self.waiting_list:
                if isinstance(person, Fellow):
                    print_str += (
                                  "\n{} {} ----- {} ----- {}"
                                  .format(person.fname, person.sname,
                                          person.role, person.wants_living)
                                  )
                elif isinstance(person, Staff):
                    print_str += ("\n{} {} ----- {}".format(
                                                           person.fname,
                                                           person.sname,
                                                           person.role))
            if option is None:
                return(print_str)
            else:
                file_txt = open("./data/" + option + ".txt", "w")
                file_txt.write(print_str)
                file_txt.close()
                return("File" + option + ".txt has been successfully created "
                       "in /data folder")
        else:
            return("There are no unallocated people nothing to output")

    def print_allocations(self, option=None):
        """
        print out people currently allocated
        to a room and the room name
        """
        rooms_w_guys = self.get_rooms_w_people()
        if len(rooms_w_guys) >= 1:
            print_str = ("\n\n" + "*"*10 + "People Allocated to Rooms" +
                         "*"*10)
            print_rmstr = ""
            for room in rooms_w_guys:
                print_rmstr += ("\n\n ** Room :{} _____Type:{}"
                                .format(room.name.upper(), room.type))
                print_rmstr += ("\n" + "-"*50 + "\n")
                member_string = ""
                for person in room.occupants:
                    member_string += ("{} {} {} ,"
                                      .format(person.fname, person.sname,
                                              person.role))
                print_rmstr += member_string
            final_prnt = print_str + print_rmstr
            if option is None:
                return final_prnt
            else:
                file_txt = open("./data/" + option + ".txt", "w")
                file_txt.write(print_str)
                file_txt.close()
                return("File" + option + ".txt has been successfully created "
                       "in /data folder")
        else:
            return("Nobody has been allocated")

    def batch_add_person(self, file_path):
        """  method to load names from txt file and add people to system """
        try:
            with open(file_path, "r") as people_file:
                for person_string in people_file:
                    person_details = person_string.rstrip().split()
                    if len(person_details) == 4:
                        self.add_person(person_details[0], person_details[1],
                                        person_details[2], person_details[3])
                    elif len(person_details) == 3:
                        self.add_person(person_details[0], person_details[1],
                                        person_details[2])
                    else:
                        return("the text file has formatting errors")
                return("People successfully added")
        except (FileNotFoundError, IOError):
            return("couldn't find file specify correct file path")

    def print_room(self, rm_name):
        """ print the occupants in a room given the room name """
        room_exists = [room for room in self.room_directory
                       if room.name.lower() == rm_name.lower()]
        if len(room_exists):
            for room in room_exists:
                members = ""
                if len(room.occupants) >= 1:
                    for person in room.occupants:
                        members += (" {} {},"
                                    .format(person.fname, person.sname))
                    return(members)
                else:
                    return("the room is empty")
        else:
            return ("the room doesn't exist")

    def save_system_state(self, database_name="sqlite_amity.db"):
        """ method to save state to database """

        conn = sqlite3.connect(database_name)
        conn.execute('''CREATE TABLE IF NOT EXISTS Amity
        (Id INTEGER PRIMARY KEY,ROOM_DIRECTORY text, WAITING_LIST text,
        PEOPLE_DIRECTORY text, LIVING_WAITING text);''')
        conn.close()

        # convert list variables to string representation for storage
        rooms_str = pickle.dumps(self.room_directory)
        waitlist_str = pickle.dumps(self.waiting_list)
        people_str = pickle.dumps(self.people_directory)
        livelist_str = pickle.dumps(self.living_waiting_list)
        conn = sqlite3.connect(database_name)
        conn.execute("INSERT OR REPLACE INTO Amity(Id, ROOM_DIRECTORY,"
                     "WAITING_LIST, PEOPLE_DIRECTORY, LIVING_WAITING) "
                     "VALUES(?, ?, ?, ?, ?);",
                     (1, rooms_str, waitlist_str, people_str, livelist_str))
        conn.commit()
        conn.close()
        status_msg = ("The data has been stored in the database: "
                      + database_name)
        return (status_msg)

    def load_system_state(self, database_name="sqlite_amity.db"):
        """ method to load state from database """
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT ROOM_DIRECTORY FROM Amity WHERE Id=1")
            room_dmp = cursor.fetchone()

            cursor.execute("SELECT WAITING_LIST FROM Amity WHERE Id=1")
            wait_dmp = cursor.fetchone()

            cursor.execute("SELECT PEOPLE_DIRECTORY FROM Amity WHERE Id=1")
            people_dmp = cursor.fetchone()

            cursor.execute("SELECT LIVING_WAITING FROM Amity WHERE Id=1")
            lwait_dmp = cursor.fetchone()

            conn.close()

            # The retrieved database values are restored to the application
            room_list = pickle.loads(room_dmp[0])
            wait_list = pickle.loads(wait_dmp[0])
            people_list = pickle.loads(people_dmp[0])
            lwait_list = pickle.loads(lwait_dmp[0])

            # the values are loaded back to the Amity session
            self.waiting_list = wait_list
            self.room_directory = room_list
            self.people_directory = people_list
            self.living_waiting_list = lwait_list
            status_msg = ("The system state has been restored from: "
                          + database_name)
            return (status_msg)
        except:
            error_msg = ("there was a problem with database: " + database_name
                         + " please confirm the database name is correct")
            return(error_msg)
