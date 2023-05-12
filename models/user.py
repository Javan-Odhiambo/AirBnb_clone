"""
Supplies the User Model class
"""
from models.base_model import BaseModel


class User(BaseModel):
    """The User model

        Attributes:
            email: (str) - empty string
            password: (str) - empty string
            first_name: (str) - empty string
            last_name: (str) - empty string
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return super().__str__()
