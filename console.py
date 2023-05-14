#!/usr/bin/python3
"""
Defines the HBnB console.
"""
import cmd
import re
from shlex import split
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


def parse_arguments(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the HBNBcommand interpreter

    Attributes:
        prompt (str): The command prompt
        __classes (dict): A dictionary of classes to be used

    Methods:
        do_quit(self, args)
            -exit the program
    """

    prompt = '(hbnb) '

    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Place": Place,
        "Amenity": Amenity,
        "Review": Review,
    }

    def create_object(self, instance):
        """Returns an object given a dictionary
        Args:
            instance: (dict) - A dictionary representation of the object.
        Return:
            An Object from a Model Class.
        """
        class_name = instance["__class__"]
        return self.__classes[class_name](**instance)

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        command_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        dot_match = re.search(r"\.", arg)
        if dot_match is not None:
            arg_parts = [arg[:dot_match.start()], arg[dot_match.end():]]
            parentheses_match = re.search(r"\((.*?)\)", arg_parts[1])
            if parentheses_match is not None:
                command_parts = [
                    arg_parts[1][:parentheses_match.start()],
                    parentheses_match.group()[1:-1]
                ]
                if command_parts[0] in command_dict:
                    arguments = "{} {}".format(arg_parts[0], command_parts[1])
                    return command_dict[command_parts[0]](arguments)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, args):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, args):
        """EOF signal to exit the program"""
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_create(self, args):
        """Creates a new instance of model class

            Args:
                (str) - Name of the class to create and instance of.
            Description:
                - Prints an error given wrong outputs.
                - On success, It prints the id of the new instance.
        """
        if not args:
            print("** class name missing **")
            return
        args = parse_arguments(args)
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return

        instance = self.__classes[class_name]()
        instance.save()
        print(instance.id)

    def do_show(self, args):
        """ Prints the string representation of an instance
            based on the class name and id.

            Args:
                (str): class name.
                (str): id fot he instance.

            Description:
                - Prints an error if given false arguments.
                - Prints an error if the instance is not found.
        """
        object_dict = storage.all()
        args = parse_arguments(args)

        if len(args) == 0:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return

        id = args[1].replace('"', '')
        key = "{}.{}".format(class_name, id)
        found = False
        for k, instance in object_dict.items():
            if k == key:
                found = True
                print(self.create_object(instance))

        if found is False:
            print("** no instance found **")

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id

            Args:
                (str): class name of the instance
                (str): id of the instance

            Description:
                - Given less arguments it prints an error.
                - Prints error if instance was not found.
        """
        if len(args.split()) == 0:
            print("** class name missing **")
            return

        class_name = args.split()[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return

        if len(args.split()) == 1:
            print("** instance id missing **")
            return

        object_dict = storage.all()
        id = args.split()[1].replace('"', '')
        key = "{}.{}".format(class_name, id)
        found = False

        for k in object_dict.keys():
            if k == key:
                found = True
                del object_dict[key]
                storage.save()
                return

        if not found:
            print("** no instance found **")

    def do_all(self, args):
        """ Prints all string representation of all instances
            based or not on the class name

            Args:
                (str) - A class name of the instances to print

            Description:
                - Given a wrong class, It prints an error.
        """
        args = parse_arguments(args)
        class_name = args[0] if args else None
        object_dict = storage.all()

        if class_name and class_name not in self.__classes:
            print("** class doesn't exist **")
        else:
            instances = []
            for obj in object_dict.values():
                if not class_name or obj["__class__"] == class_name:
                    instances.append(str(self.create_object(obj)))
            print(instances)

    def do_update(self, args):
        """ Updates an instance based on the class name
            and id by adding or updating attribute

            Args:
                (str): class name.
                (str): object id.
                (str): attribute name.
                (str): value name.

            Description:
                - Prints different errors if given the wrong input.
                - Prints an error if the instance is not stored.
        """
        args = parse_arguments(args)
        class_name = args[0] if args else None
        dictionary = True if type(eval(args[2])) is dict else False
        if class_name is None:
            print("** class name missing **")
            return
        if class_name and class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4 and not dictionary:
            print("** value missing **")
            return
        instance_id = args[1]
        obj_key = "{}.{}".format(class_name, instance_id)
        object_dict = storage.all()
        if obj_key not in object_dict:
            print("** no instance found **")
            return
        instance = object_dict[obj_key]
        if dictionary:
            the_dict = eval(args[2])
            for k, val in the_dict.items():
                if k in ["id", "created_at", "updated_at"]:
                    return
                instance[k] = val
        else:
            attribute_name = args[2]
            attribute_value = args[3].strip('"')
            if attribute_value.isdigit():
                attribute_value = int(attribute_value)
            if len(args) == 4:
                if attribute_name in ["id", "created_at", "updated_at"]:
                    return
                instance[attribute_name] = attribute_value
        storage.save()

    def do_count(self, args):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        args = parse_arguments(args)
        class_name = args[0]
        count = 0
        for instance in storage.all().values():
            if instance['__class__'] == class_name:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
