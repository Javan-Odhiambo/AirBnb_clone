"""
Supplies the FileStorage class.
"""
import json


class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file to instances:
        Private class attributes:
            __file_path: (str) - path to the JSON file
            __objects: (dict) - empty but will store all objects by <class name>.id
                                (ex: to store a BaseModel object with id=12121212,
                                the key will be BaseModel.12121212)
        Public instance methods:
            all(self): returns the dictionary _objects
            new(self, obj): sets in __objects the obj with key <class name>.id
            save(self): serializes __objects to JSON file
            reload(self): deserializes the JSON file to __objects
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """Returns a dictionary of all existing objects

        Returns:
            self.__objects: (dict) - Contains all objects.
        """
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <class name>.id
        """
        if obj and obj.id:
            key = type(obj).__name__ + '.' +  obj.id
            self.__objects[key] = obj.to_dict()

    def save(self):
        """Serializes __objects to JSON file
        """
        if self.__objects:
            with open(self.__file_path, "w") as file:
                json.dump(self.__objects, file)

    def reload(self):
        """Deserializes the JSON file to __objects

            Description:
                if the JSON file (__file_path) exists:
                    deserializes the JSON file to __objects
                otherwise:
                    do nothing.

                If the file doesn't exist:
                    no exception should be raised)
        """
        try:
            with open(self.__file_path, 'r') as file:
                self.__objects = json.load(file)
        except FileNotFoundError:
            pass
