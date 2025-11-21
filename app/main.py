from fastapi import FastAPI
from app.database import Base, engine
from app import models, routes

# Création des tables
Base.metadata.create_all(bind=engine)

# Création de l'application FastAPI
app = FastAPI(
    title="EcoTrack API",
    description="API for tracking CO2 emissions and air quality data",
    version="1.0.0"
)

# Inclusion des routes
if hasattr(routes, 'router'):
    app.include_router(routes.router)
