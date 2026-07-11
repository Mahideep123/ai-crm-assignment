from sqlalchemy import Column, Integer, String, DateTime
import datetime
from database import Base

class HCP(Base):
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    specialty = Column(String(255))
    location = Column(String(255))

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(1000))
    efficacy = Column(String(1000))

# We can also add an Interaction table, but the primary logic 
# relies on the Redux state in the frontend. If we need to persist,
# we would add it here.
class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String(255))
    interaction_type = Column(String(50))
    date = Column(String(50))
    time = Column(String(50))
    attendees = Column(String(500))
    topics = Column(String(1000))
    materials = Column(String(1000))
    samples = Column(String(1000))
    sentiment = Column(String(50))
    outcomes = Column(String(1000))
    follow_up = Column(String(1000))
