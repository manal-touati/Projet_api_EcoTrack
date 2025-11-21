from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# URL de la base (SQLite ici)
SQLALCHEMY_DATABASE_URL = "sqlite:///./ecotrack.db"

# Création du moteur
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # nécessaire pour SQLite + FastAPI
)

# Session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()


# Dépendance : récupérer une session et la fermer proprement
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
