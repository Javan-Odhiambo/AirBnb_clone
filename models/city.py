"""
Supplies the City Model class
"""
from models.base_model import BaseModel


class City(BaseModel):
    """The City model

        Attributes:
            state_id: (str) - empty string
            name: (str) - empty string

    """
    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return super().__str__()
