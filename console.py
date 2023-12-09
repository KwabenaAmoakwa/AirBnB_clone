#!/usr/bin/python3
"""Command Interpreter document"""

import cmd
from models.base_model import BaseModel
from models import storage
import json
import re


class HBNBCommand(cmd.Cmd):
    "Class of my command intepreter"
    prompt = "(hnnb) "

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """Cntrl + D to quit the program"""
        return True

    def emptyline(self):
        """Override default empty line"""
        return False

    def do_create(self, line):
        """Create a new instance of Basemodel"""
        if line == "" or line is None:
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class doesn't exist **")
        else:
            new_inst = storage.classes()[line]()
            new_inst.save()
            print(new_inst.id)

    def do_show(self, line):
        """Print string representation of an instance"""
        if line == "" or line is None:
            print("** class name missing **")
            return

        words = line.split(" ")
        if words[0] not in storage.classes():
            print("** class doesn't exist **")
        elif len(words) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(words[0], words[1])
            if key not in storage.all():
                print("** no instance found **")
            else:
                print(storage.all()[key])

    def do_destroy(self, line):
        """Delete all instances based on class name and id"""
        if line is None or line == "":
            print("** class name missing **")
            return
        comm = line.split()

        if comm[0] not in storage.classes():
            print("** class doesn't exist **")
        elif len(comm) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(comm[0], comm[1])
            if key not in storage.all():
                print("** no instance found **")
            else:
                del storage.all()[key]
                storage.save()

    def do_all(self, line):
        """Prints all string reps of all instances"""
        if line is not None or line != "":
            comm = line.split()

            if comm[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                new = [
                    str(obj)
                    for key, obj in storage.all().items()
                    if type(obj).__name__ == comm[0]
                ]
                print(new)
        else:
            new_list = [str(obj) for key, obj in storage.all().items()]
            print(new_list)

    import re

    def do_update(self, line):
        """Updates an instance by adding or updating attribute."""
        if not line or line == "":
            print("** class name missing **")
            return

        regex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(regex, line)

        if not match:
            print("** invalid input format **")
            return

        classname = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        
        if classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)

            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', value):
                    if "." in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass 
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()                       
        

if __name__ == "__main__":
    HBNBCommand().cmdloop()
