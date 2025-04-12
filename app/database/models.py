from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    seats = Column(Integer)
    location = Column(String)

    reservations = relationship("Reservation", back_populates="table")

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    table_id = Column(Integer, ForeignKey('tables.id'))  # Указываем связь с таблицей
    reservation_time = Column(DateTime)
    duration_minutes = Column(Integer)

    table = relationship("Table", back_populates="reservations")



