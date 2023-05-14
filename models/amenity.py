#!/usr/bin/python3
"""
Supplies the Amenity Model class
"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """The Amenity model

        Attributes:
            name: (str) - empty string

    """
    name = ""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return super().__str__()
