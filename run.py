#!/usr/bin/env python
"""
This is the Interactive Amity room allocation Command line interface
Usage:
    Amity create_room <room_type> <room_name>...
    Amity add_person <first_name> <second_name> <role> [<wants_accommodation>]
    Amity print_room <room_name>
    Amity print_unallocated [--o=filename]
    Amity print_allocations [--o=filename]
    Amity load_people <file_path>
    Amity get_id <first_name> <second_name>
    Amity reallocate_person <person_identifier> <new_room_name>
    Amity save_state [--db=sqlite_database]
    Amity load_state <sqlite_database>
    Amity (-i | --interactive)
    Amity (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Shows the available commands for Amity.
"""

import cmd
from docopt import docopt, DocoptExit
from app import Amity
from termcolor import cprint
from pyfiglet import figlet_format


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


def intro():
    cprint(figlet_format('Amity Room Allocation System', font='slant'),
           'blue', attrs=['bold'])
    print("Welcome to Amity! Here is a list of commands to get you started." +
          " Type 'help' anytime to access available commands")
    cprint(__doc__, 'green')


class AmityInterface (cmd.Cmd):
    intro()
    prompt = 'Amity ->>'

    amity = Amity()

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room <room_type> <room_name>..."""
        rm_type = arg["<room_type>"]
        rm_name = arg["<room_name>"]
        print(self.amity.add_room(rm_type, rm_name))
        self.amity.allocate()

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
        print(self.amity.print_room(arg["<room_name>"]))

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <first_name> <second_name> <role>
        [<wants_accommodation>]"""
        fname = arg["<first_name>"]
        sname = arg["<second_name>"]
        role = arg["<role>"]
        wants_acc = arg["<wants_accommodation>"]
        if wants_acc:
            self.amity.add_person(fname, sname, role, wants_acc)
        else:
            self.amity.add_person(fname, sname, role)

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [--o=filename]"""
        option = arg["--o"]
        if option:
            print(self.amity.print_unallocated(option))
        else:
            print(self.amity.print_unallocated())

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people <file_path>"""
        print(self.amity.batch_add_person(arg["<file_path>"]))
        self.amity.allocate()

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocated [--o=filename]"""
        option = arg["--o"]
        if option:
            print(self.amity.print_allocations(option))
        else:
            print(self.amity.print_allocations())

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_identifier> <new_room_name>"""
        person_id = arg["<person_identifier>"]
        new_room = arg["<new_room_name>"]
        print(self.amity.reallocate(int(person_id), new_room))

    @docopt_cmd
    def do_get_id(self, arg):
        """
        return the unique identifier given search terms
        Usage: get_id <first_name> <second_name>
        """
        fname = arg["<first_name>"]
        sname = arg["<second_name>"]
        print(self.amity.get_person_id(fname, sname))

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=sqlite_database]"""
        option = arg["--db"]
        if option:
            print(self.amity.save_system_state(option))
        else:
            print(self.amity.save_system_state())

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state <sqlite_database>"""
        database = arg["<sqlite_database>"]
        print(self.amity.load_system_state(database))

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()


if __name__ == '__main__':
    try:
        AmityInterface().cmdloop()
    except KeyboardInterrupt:
        print('Exiting Application')
