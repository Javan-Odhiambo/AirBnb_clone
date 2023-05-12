#!/usr/bin/python3
"""
Defines the HBnB console.
"""
import cmd
from models import storage
from models.base_model import BaseModel


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
    }

    '''
    Final __classes dict
     __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Place": Place,
        "Amenity": Amenity,
        "Review": Review,
    }
    '''

    def do_quit(self, args):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, args):
        """EOF signal to exit the program"""
        print("")
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_create(self, args):
        """Creates a new instance of BaseModel"""
        if not args:
            print("** class name missing **")
            return
        class_name = args.split()[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        instance = self.__classes[class_name]()
        instance.save()
        print(instance.id)

    def do_show(self, args):
        """ Prints the string representation of an instance
            based on the class name and id
        """
        object_dict = storage.all()
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
        id = args.split()[1]
        key = "{}.{}".format(class_name, id)
        found = False
        for k, instance in object_dict.items():
            if k == key:
                found = True
                print(instance)
        if found is False:
            print("** no instance found **")

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id"""
        object_dict = storage.all()
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
        id = args.split()[1]
        key = "{}.{}".format(class_name, id)
        found = False
        for k in list(object_dict.keys()):
            if k == key:
                found = True
                del object_dict[key]
                storage.save()
                return
        if not found:
            print("** no instance found **")

    def do_all(self, args):
        """ Prints all string representation of all instances
            based or not on the class name"""
        class_name = args.split()[0] if args else None
        object_dict = storage.all()
        if class_name and class_name not in self.__classes:
            print("** class doesn't exist **")
        else:
            instances = []
            for obj in object_dict.values():
                if not class_name or obj.__class__.__name__ == class_name:
                    instances.append(obj.__str__())
            print(instances)

    def do_update(self, args):
        """ Updates an instance based on the class name
            and id by adding or updating attribute"""
        class_name = args.split()[0] if args else None
        args = args.split()
        if class_name is None:
            print("** class name missing **")
            return
        if class_name and class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        if len(args) < 3:
            print("** attribute name missing **")
            return
        attribute_name = args[2]
        if len(args) < 4:
            print("** value missing **")
            return
        attribute_value = args[3].strip('"')
        if attribute_value.isdigit():
            print("Yes")
            attribute_value = int(attribute_value)
        object_dict = storage.all()
        obj_key = "{}.{}".format(class_name, instance_id)
        if obj_key not in object_dict:
            print("** no instance found **")
            return
        if len(args) == 4:
            instance = object_dict[obj_key]
            if attribute_name in ["id", "created_at", "updated_at"]:
                return
            instance[attribute_name] = attribute_value
            storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
