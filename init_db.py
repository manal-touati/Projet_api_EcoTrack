import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import bcrypt
from app.models import Base, Emission, AirQuality, Source, User

# Configuration de la base de données
DATABASE_URL = "sqlite:///./ecotrack.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_database():
    """Initialise la base de données et charge les données"""
    
    print("Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès")
    
    db = SessionLocal()
    
    try:
        # 1. Charger les émissions CO2
        print("\nChargement des émissions CO2...")
        df_emissions = pd.read_csv('data/co2_emissions_by_sector.csv')
        
        emissions_count = 0
        for _, row in df_emissions.iterrows():
            emission = Emission(
                country=row['country'],
                sector=row['sector'],
                date=pd.to_datetime(row['date']).date(),
                value=float(row['value'])
            )
            db.add(emission)
            emissions_count += 1
            
            if emissions_count % 10000 == 0:
                print(f"   {emissions_count} émissions chargées...")
        
        db.commit()
        print(f"{emissions_count} émissions CO2 chargées")
        
        # 2. Charger les données de qualité de l'air
        print("\nChargement des données de qualité de l'air...")
        df_air = pd.read_csv('data/global_air_quality.csv')
        
        air_count = 0
        for _, row in df_air.iterrows():
            air_quality = AirQuality(
                city=row['city'],
                country=row['country'],
                date=pd.to_datetime(row['date']).date(),
                pm25=float(row['pm25']),
                pm10=float(row['pm10']),
                no2=float(row['no2']),
                so2=float(row['so2']),
                co=float(row['co']),
                o3=float(row['o3'])
            )
            db.add(air_quality)
            air_count += 1
            
            if air_count % 1000 == 0:
                print(f"   {air_count} mesures de qualité de l'air chargées...")
        
        db.commit()
        print(f"{air_count} mesures de qualité de l'air chargées")
        
        # 3. Créer les sources de données
        print("\nCréation des sources de données...")
        sources = [
            Source(
                name="CO2 Emissions by Sector",
                description="Dataset global des émissions de CO2 par secteur d'activité",
                url="https://www.kaggle.com/datasets/emissions-co2-sector",
                data_type="emissions"
            ),
            Source(
                name="Global Air Quality Database",
                description="Base de données mondiale de la qualité de l'air (WHO)",
                url="https://www.who.int/data/gho/data/themes/air-pollution",
                data_type="air_quality"
            )
        ]
        
        for source in sources:
            db.add(source)
        
        db.commit()
        print(f"{len(sources)} sources ajoutées")
        
        # 4. Créer un utilisateur admin par défaut
        print("\nCréation de l'utilisateur admin...")
        admin_password = "admin123"
        hashed_password = bcrypt.hashpw(admin_password[:72].encode('utf-8'), bcrypt.gensalt())
        
        admin = User(
            username="admin",
            email="admin@ecotrack.com",
            hashed_password=hashed_password.decode('utf-8'),
            role="admin"
        )
        db.add(admin)
        
        # Créer un utilisateur test
        user_password = "user123"
        hashed_user_password = bcrypt.hashpw(user_password[:72].encode('utf-8'), bcrypt.gensalt())
        
        user = User(
            username="testuser",
            email="user@ecotrack.com",
            hashed_password=hashed_user_password.decode('utf-8'),
            role="user"
        )
        db.add(user)
        
        db.commit()
        print("Utilisateurs créés")
        print("   Admin: admin@ecotrack.com / admin123")
        print("   User:  user@ecotrack.com / user123")
        
        print("\nBase de données initialisée avec succès !")
        print(f"\nStatistiques:")
        print(f"   - Émissions CO2: {emissions_count}")
        print(f"   - Qualité de l'air: {air_count}")
        print(f"   - Sources: {len(sources)}")
        print(f"   - Utilisateurs: 2")
        
    except Exception as e:
        print(f"\nErreur lors de l'initialisation: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Initialisation de la base de données EcoTrack\n")
    init_database()
