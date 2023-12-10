#!/usr/bin/python3
"""Contains File storing the projects data"""

import json
import os
import datetime


class FileStorage:
    """File storage class"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in object the the key and value"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def classes(self):
        """Returns a dictionary of valid classes and their references"""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review,
        }
        return classes

    def save(self):
        """Serializes object to a json file"""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as file:
            dic = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
            json.dump(dic, file)

    def reload(self):
        """Deserializes a json file to python object"""
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as file:
            dict_object = json.load(file)
            dict_object = {
                k: self.classes()[v["__class__"]](**v) for k, v in dict_object.items()
            }
            FileStorage.__objects = dict_object

    def attributes(self):
        """Returns the valid attributes and their types for classname"""
        attributes = {
            "BaseModel": {
                "id": str,
                "created_at": datetime.datetime,
                "updated_at": datetime.datetime,
            },
            "User": {
                "email": str,
                "password": str,
                "first_name": str,
                "last_name": str,
            },
            "State": {"name": str},
            "City": {"state_id": str, "name": str},
            "Amenity": {"name": str},
            "Place": {
                "city_id": str,
                "user_id": str,
                "name": str,
                "description": str,
                "number_rooms": int,
                "number_bathrooms": int,
                "max_guest": int,
                "price_by_night": int,
                "latitude": float,
                "longitude": float,
                "amenity_ids": list,
            },
            "Review": {"place_id": str, "user_id": str, "text": str},
        }
        return attributes
