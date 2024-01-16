#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime(), nullable=False, default= datetime.utcnow())
    updated_at = Column(DateTime(), nullable=False, default= datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                elif key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        dict = self.__dict__.copy()
        dict.pop("_sa_instance_state", None)
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, (dict))

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        from models import storage
        storage.new(self)
        storage.save()

    def delete(self):
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """Convert instance into dict format"""
        output = self.__dict__.copy()
        output['__class__'] = self.__class__.__name__
        if "created_at" in output.keys():
            output['created_at'] = output['created_at'].isoformat()
        if "updated_at" in output.keys():
            output['updated_at'] = output['updated_at'].isoformat()
        if "_sa_instance_state" in output.keys():
            del output['_sa_instance_state']
        return output
