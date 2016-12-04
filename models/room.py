class Amity(object):
    def __init__(self, name, capacity=0, status="open"):
        self.capacity = capacity

class Room(Amity):
    def __init__(self):
        super(Amity, self).__init__(name)

class Office(Room):
    def __init__(self, capacity=6):
        super(Office, self).__init__(name)
        self.capacity = capacity

 class LivingSpace(Room):
     def __init__(self, capacity=4):
         super(LivingSpace, self).__init(name)
         self.capacity = capacity
