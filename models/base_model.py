"""
Supplies the BaseModel class.
"""
from uuid import uuid4
from datetime import datetime

from models import storage


class BaseModel:
    """Defines all common attributes/methods for other classes.

    Attributes:
        id: (str) - assign with an uuid when an instance is created:
        created_at: (datetime) - assigned when an instance is created
        updated_at: (datetime) - updated every time you change your object

    Methods:
        save(self):
            - updates the updated_at attribute with the current datetime.
        to_dict(self):
            - gives a dictionary containing all attributes and values.

    """
    def __init__(self, *args, **kwargs) -> None:
        """Instantiates a new object
            Description:
                - If kwargs is not empty, all the keys are set as attributes.
                - Else a default object is instantiated.
        """
        if kwargs:
            date_format = '%Y-%m-%dT%H:%M:%S.%f'
            for key, val in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    val = datetime.strptime(val, date_format)
                if key != '__class__':
                    setattr(self, key, val)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self) -> str:
        """String representation of the object.

            Returns:
                - (str) - [<class name>] (<self.id>) <self.__dict__>
        """
        return "[{}] ({}) {}".format(
                                type(self).__name__,
                                self.id, self.__dict__)

    def save(self) -> None:
        """updates the updated_at attribute with the current datetime.
        """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self) -> dict:
        """Returns a dictionary containing all key/values of the instance

        Description:
            - uses self.__dict__, so that only set attributes are be returned
            - __class__ is added to the dict with the class name as the value
            - created_at and updated_at are be converted to str object.
                - format: %Y-%m-%dT%H:%M:%S.%f (ex: 2017-06-14T22:31:03.285259)
        Returns:
            dict: the dictionary containing all set attributes.
        """
        model_dict = {}
        model_dict['__class__'] = type(self).__name__

        for key, val in self.__dict__.items():
            if key == 'created_at' or key == 'updated_at':
                val = val.isoformat()

            model_dict[key] = val

        return (model_dict)
