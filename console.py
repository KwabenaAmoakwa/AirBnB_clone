#!/usr/bin/python3
"""Command Interpreter document"""

import cmd
from models.base_model import BaseModel
from models import storage
import json
import re


class HBNBCommand(cmd.Cmd):
    "Class of my command intepreter"
    prompt = "(hbnb) "

    def default(self, line):
        """Catch commands if nothing else matches them"""
        self._precmd(line)

    def _precmd(self, line):
        """Intercepts commands to test for class.syntax()"""
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line
        classname = match.group(1)
        method = match.group(2)
        args = match.group(3)
        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search("^({.*})$", attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict
            )
            if match_attr_and_value:
                attr_and_value = (
                    (match_attr_and_value.group(1) or "")
                    + " "
                    + (match_attr_and_value.group(2) or "")
                )
        command = method + " " + classname + " " + uid + " " + attr_and_value
        self.onecmd(command)
        return command

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """Cntrl + D to quit the program"""
        return True

    def emptyline(self):
        """Override default empty line"""
        pass

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
                    value = value.replace('"', "")
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

    def do_count(self, line):
        """Counts the instances of a class"""
        command = line.split(" ")
        if not command[0]:
            print("** class name missing **")
        elif command[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            no_instances = [k for k in storage.all() if k.startswith(command[0] + ".")]
            print(len(no_instances))


if __name__ == "__main__":
    HBNBCommand().cmdloop()
