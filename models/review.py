"""
Supplies the Review Model class
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """The Review model

        Attributes:
            place_id: (str) - empty string: it will be the Place.id
            user_id: (str) - empty string: it will be the User.id
            text: (str) - empty string
    """
    place_id = ""
    user_id = ""
    text = ""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return super().__str__()
