#! #! usr/bin/env
"""
    This module implements Amity as a class based interface for the entire
    room allocation system
"""

import sys

sys.path.append("./models")

from person import Fellow, Staff
from room import Office, LivingSpace


class Amity(object):
    def __init__(self):
        pass
