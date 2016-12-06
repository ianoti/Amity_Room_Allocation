#! usr/bin/env
class Room(object):
    def __init__(self, name, capacity=0, access_allowed=[], occupants=[]):
        self.name = name
        self.capacity = capacity
        self.access_allowed = access_allowed
        self.occupants = occupants

class Office(Room):
    def __init__(self, name):
        super(Office, self).__init__(name)
        self.capacity = 6
        self.access_allowed = ["fellow", "staff"]

class LivingSpace(Room):
    def __init__(self, name):
        super(LivingSpace, self).__init__(name)
        self.capacity = 4
        self.access_allowed = ["fellow"]
