from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import Base, engine
from app import models, routes
import os

# Création des tables
Base.metadata.create_all(bind=engine)

# Création de l'application FastAPI
app = FastAPI(
    title="EcoTrack API",
    description="API for tracking CO2 emissions and air quality data",
    version="1.0.0"
)

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes API
if hasattr(routes, 'router'):
    app.include_router(routes.router)

# Servir le frontend sur /dashboard
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")
    
    @app.get("/dashboard")
    async def read_dashboard():
        return FileResponse(os.path.join(frontend_path, "index.html"))
