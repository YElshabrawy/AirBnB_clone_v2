#!/usr/bin/python3
""" Place Module for HBNB project """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
import os
from models.amenity import Amenity
import models


place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'),
           primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'),
           primary_key=True, nullable=False),
)


class Place(BaseModel, Base):
    """A place to stay."""

    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship('Review', backref='place',  cascade='delete')
    amenity_ids = []
    amenities = relationship('Amenity', secondary='place_amenity',
                             overlaps="place_amenities", viewonly=False)

    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """ Getter for Place's Reviews """
            reviews = []
            for review in self.reviews:
                if review.place_id == self.id:
                    reviews.append(review)
            return reviews

        @property
        def amenities(self):
            """ Getter for Place's Amenities"""
            amenities = []
            for amenity in models.storage.all(Amenity).values():
                if amenity.id in self.amenity_ids:
                    amenities.append(amenity)
            return amenities

        @amenities.setter
        def amenities(self, amenity):
            """Setter for Amenities"""
            if type(amenity) == Amenity:
                self.amenity_ids.append(amenity.id)
