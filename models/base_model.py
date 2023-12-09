#!/usr/bin/python3
"""This base model is inherited by other models in this project"""

from datetime import datetime
import uuid
from models import storage


class BaseModel:
    """Base model class"""

    def __init__(self, *args, **kwargs):
        """Instantiation process"""
        if kwargs is not None and kwargs != {}:
            for key in kwargs:
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f"
                    )
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f"
                    )

                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Prints string representation of instance"""
        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """Updates the attribute updated at with the current datetime"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Dictionary representation of the object"""
        dic_obj = self.__dict__.copy()
        dic_obj["__class__"] = type(self).__name__
        dic_obj["created_at"] = self.created_at.isoformat()
        dic_obj["updated_at"] = self.updated_at.isoformat()
        return dic_obj
