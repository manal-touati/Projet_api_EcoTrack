from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

# Modèle Emissions pour CO2 Emissions by sector
class Emission(Base):
    __tablename__ = "co2_emissions_by_sector"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, index=True)
    date = Column(Date)
    sector = Column(String)
    value = Column(Float)
    timestamp = Column(Integer)

    # Relation vers la source
    source_id = Column(Integer, ForeignKey("sources.id"))
    source = relationship("Source", back_populates="emissions")


# Modèle Global pour Global air quality
class Global(Base):
    __tablename__ = "global_air_quality"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    country = Column(String, index=True)
    date = Column(Date)

    pm25 = Column(Float)
    pm10 = Column(Float)
    no2 = Column(Float)
    so2 = Column(Float)
    co = Column(Float)
    o3 = Column(Float)

    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)

    # Relation vers source
    source_id = Column(Integer, ForeignKey("sources.id"))
    source = relationship("Source", back_populates="global_data")


# Modèle users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, nullable=False, default='user')
    created_at = Column(DateTime, default=datetime.utcnow)


# Modèle Source pour métadonnées d'origine
class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    origin = Column(String)
    description = Column(String)

    # Relations vers les datasets
    emissions = relationship("Emission", back_populates="source")
    global_data = relationship("Global", back_populates="source")
