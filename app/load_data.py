import pandas as pd
import sys
from pathlib import Path
from sqlalchemy.orm import Session
from datetime import datetime

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, engine
from app.models import Emission, Global, Source, Base

# Créer les tables
Base.metadata.create_all(bind=engine)

# Charger les données
db = SessionLocal()

try:
    # ===== CHARGER LES SOURCES =====
    print("Chargement des sources...")
    
    # Source pour CO2 emissions
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
        print("Source CO2 créée")
    else:
        print("Source CO2 déjà présente")
    
    # Source pour Air Quality
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
        print("Source Air Quality créée")
    else:
        print("Source Air Quality déjà présente")
    
    
    # ===== CHARGER CO2 EMISSIONS =====
    print("\nChargement des émissions CO2...")
    data_co2 = pd.read_csv("data/co2_emissions_by_sector.csv")
    
    inserted_co2 = 0
    skipped_co2 = 0
    
    for _, row in data_co2.iterrows():
        # Convertir la date (format DD/MM/YYYY)
        date_obj = datetime.strptime(row['date'], '%d/%m/%Y').date()
        
        # Vérifier si existe déjà
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
            
            # Commit par batch de 1000 pour performance
            if inserted_co2 % 1000 == 0:
                db.commit()
                print(f"  → {inserted_co2} émissions insérées...")
        else:
            skipped_co2 += 1
    
    db.commit()
    print(f"{inserted_co2} émissions CO2 insérées, {skipped_co2} déjà présentes")
    
    
    # ===== CHARGER GLOBAL AIR QUALITY =====
    print("\nChargement de la qualité de l'air...")
    data_air = pd.read_csv("data/global_air_quality.csv")
    
    inserted_air = 0
    skipped_air = 0
    
    for _, row in data_air.iterrows():
        # Convertir la date (format YYYY-MM-DD)
        date_obj = datetime.strptime(row['Date'], '%Y-%m-%d').date()
        
        # Vérifier si existe déjà
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
            
            # Commit par batch de 1000 pour performance
            if inserted_air % 1000 == 0:
                db.commit()
                print(f"  → {inserted_air} mesures insérées...")
        else:
            skipped_air += 1
    
    db.commit()
    print(f"{inserted_air} mesures de qualité d'air insérées, {skipped_air} déjà présentes")
    
    
    # ===== RÉSUMÉ =====
    print("\n" + "="*50)
    print("RÉSUMÉ DU CHARGEMENT")
    print("="*50)
    print(f"Sources: {db.query(Source).count()} total")
    print(f"Émissions CO2: {db.query(Emission).count()} total")
    print(f"Qualité d'air: {db.query(Global).count()} total")
    print("="*50)
    
except Exception as e:
    print(f"\nErreur: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
    print("\nConnexion fermée")
