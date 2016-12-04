"""
    This File contains the class definitions handling the
    Staff and Fellows along with their attributes
"""
class Person(object):
    def __init__(self, name, location="unallocated", access="none"):
        self.name = name
        self.location = location
        self.access = access

class Fellow(Person):
    def __init__(self, name):
        super(Fellow, self).__init__(name)
        self.access = "fellow"

class Staff(Person):
    def __init__(self, name):
        super(Staff, self).__init__(name)
        self.access = "staff"
