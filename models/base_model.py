'''
Supplies the BaseModel class.
'''
from uuid import uuid4
from datetime import datetime


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
    def __init__(self) -> None:
        """Instantiates a new object
        """
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

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
        json = self.__dict__
        json['__class__'] = type(self).__name__
        json['created_at'] = json['created_at'].isoformat()
        json['updated_at'] = json['updated_at'].isoformat()

        return (json)
