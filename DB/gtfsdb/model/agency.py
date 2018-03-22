from sqlalchemy import Column, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String

from gtfsdb import config
from gtfsdb.model.base import Base


class Agency(Base):
    datasource = config.DATASOURCE_GTFS
    filename = 'agency.txt'

    __tablename__ = 'agency'

    id = Column(Integer, Sequence(None, optional=True), primary_key=True, nullable=True)
    agency_id = Column(String(40), index=True, unique=True)
    agency_name = Column(String(255), nullable=False)
    agency_url = Column(String(255), nullable=False)
    routes = relationship(
        'Route',
        primaryjoin='Route.agency_id==Agency.agency_id',
        foreign_keys='(Agency.agency_id)',
        uselist=True, viewonly=True)

    # These fields are avlible in the GTFS specs but in the Israeli files
    # agency_timezone = Column(String(50), nullable=False)
    # agency_lang = Column(String(10))
    # agency_phone = Column(String(50))
    # agency_fare_url = Column(String(255))

