#! usr/bin/env
"""
    This File contains the class definitions handling the
    Staff and Fellows along with their attributes
"""
class Person(object):
    def __init__(self, fname, sname, role="none", p_id = 0):
        self.fname = fname
        self.sname = sname
        self.role = role
        self.p_id = p_id

class Fellow(Person):
    def __init__(self, fname, sname, role, wants_living="N"):
        super(Fellow, self).__init__(fname, sname)
        self.role = "fellow"
        self.wants_living = wants_living


class Staff(Person):
    def __init__(self, fname, sname):
        super(Staff, self).__init__(fname, sname)
        self.role = "staff"
