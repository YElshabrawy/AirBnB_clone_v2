#!/usr/bin/python3
"""This module defines a class to manage db for hbnb clone"""
from os import environ
from typing import List
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """This class manages storage of hbnb models in mysql db"""
    __engine = None
    __session = None

    def __init__(self) -> None:
        db_user = environ["HBNB_MYSQL_USER"]
        db_pass = environ["HBNB_MYSQL_PWD"]
        db_host = environ.get("HBNB_MYSQL_HOST", "localhost")
        db_name = environ["HBNB_MYSQL_DB"]
        url = "mysql+mysqldb://{}:{}@{}/{}".format(db_user,
                                                   db_pass,
                                                   db_host,
                                                   db_name)
        self.__engine = create_engine(url, pool_pre_ping=True)

        if environ.get("HBNB_ENV", "") == "test":
            metadata = MetaData(bind=self.__engine)
            metadata.drop_all()

    def all(self, cls=None):
        """Query all"""
        from models.classes import CLASSES
        output = {}
        total = []
        if cls:
            res = self.__session.query(CLASSES[cls]).all()
            total.extend(res)
        else:
            for val in CLASSES.values():
                res = self.__session.query(val).all()
                total.extend(res)
        for clss in total:
            k = clss.__class__.__name__ + "." + clss.id
            output[k] = clss
        return output

    def new(self, obj):
        '''add obj to db'''
        self.__session.add(obj)

    def save(self):
        '''commit to db'''
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        from models.base_model import BaseModel, Base
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)
