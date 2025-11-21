import pandas as pd
import sys
from pathlib import Path
from sqlalchemy.orm import Session
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, engine
from app.models import Emission, Global, Source, Base

Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # CHARGER LES SOURCES
    source_co2 = db.query(Source).filter(Source.name == "CO2 Emissions Dataset").first()
    if not source_co2:
        source_co2 = Source(
            name="CO2 Emissions Dataset",
            origin="Carbon Monitor",
            description="Daily CO2 emissions by sector and country"
        )
        db.add(source_co2)
        db.commit()
        db.refresh(source_co2)
    
    source_air = db.query(Source).filter(Source.name == "Global Air Quality Dataset").first()
    if not source_air:
        source_air = Source(
            name="Global Air Quality Dataset",
            origin="Environmental Monitoring Network",
            description="Global air quality measurements with pollutant levels"
        )
        db.add(source_air)
        db.commit()
        db.refresh(source_air)
    
    # CHARGER CO2 EMISSIONS
    data_co2 = pd.read_csv("data/co2_emissions_by_sector.csv")
    
    inserted_co2 = 0
    skipped_co2 = 0
    
    for _, row in data_co2.iterrows():
        date_obj = datetime.strptime(row['date'], '%d/%m/%Y').date()
        
        existing = db.query(Emission).filter(
            Emission.country == row['country'],
            Emission.date == date_obj,
            Emission.sector == row['sector']
        ).first()
        
        if not existing:
            emission = Emission(
                country=row['country'],
                date=date_obj,
                sector=row['sector'],
                value=float(row['value']),
                timestamp=int(row['timestamp']),
                source_id=source_co2.id
            )
            db.add(emission)
            inserted_co2 += 1
            
            if inserted_co2 % 1000 == 0:
                db.commit()
        else:
            skipped_co2 += 1
    
    db.commit()
    
    # CHARGER GLOBAL AIR QUALITY
    data_air = pd.read_csv("data/global_air_quality.csv")
    
    inserted_air = 0
    skipped_air = 0
    
    for _, row in data_air.iterrows():
        date_obj = datetime.strptime(row['Date'], '%Y-%m-%d').date()
        
        existing = db.query(Global).filter(
            Global.city == row['City'],
            Global.country == row['Country'],
            Global.date == date_obj
        ).first()
        
        if not existing:
            air_quality = Global(
                city=row['City'],
                country=row['Country'],
                date=date_obj,
                pm25=float(row['PM2.5']),
                pm10=float(row['PM10']),
                no2=float(row['NO2']),
                so2=float(row['SO2']),
                co=float(row['CO']),
                o3=float(row['O3']),
                temperature=float(row['Temperature']),
                humidity=float(row['Humidity']),
                wind_speed=float(row['Wind Speed']),
                source_id=source_air.id
            )
            db.add(air_quality)
            inserted_air += 1
            
            if inserted_air % 1000 == 0:
                db.commit()
        else:
            skipped_air += 1
    
    db.commit()
    
except Exception as e:
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
