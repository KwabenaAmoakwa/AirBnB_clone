#!/usr/bin/python3
"""Review of the User"""

from models.base_model import BaseModel


class Review(BaseModel):
    """Review object"""

    place_id = ""
    user_id = ""
    text = ""
