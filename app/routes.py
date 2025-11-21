from fastapi import APIRouter, Depends, HTTPException, status, Query, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime, timedelta
from jose import JWTError, jwt

from app.database import get_db
from app import crud, schemas

router = APIRouter()
security = HTTPBearer()

SECRET_KEY = "keep_it_secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

    #Créer un token JWT
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):

    #Vérifier le token JWT
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")


def get_current_active_admin(user=Depends(verify_token)):

    #Vérifier que l'utilisateur est admin
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Accès interdit - Admin uniquement")
    return user


# EMISSIONS CO2
@router.get("/emissions", response_model=List[schemas.EmissionResponse], tags=["Emissions"])
def get_emissions(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre maximum d'éléments à retourner"),
    country: Optional[str] = Query(None, description="Filtrer par pays"),
    sector: Optional[str] = Query(None, description="Filtrer par secteur"),
    date_from: Optional[date] = Query(None, description="Date de début (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="Date de fin (YYYY-MM-DD)"),
    order_by: Optional[str] = Query(None, description="Champ de tri (préfixer par '-' pour décroissant)"),
    db: Session = Depends(get_db)
):
    #Récupérer la liste des émissions CO2 avec filtres optionnels
    filters = {}
    if country:
        filters["country"] = country
    if sector:
        filters["sector"] = sector
    if date_from:
        filters["date_from"] = date_from
    if date_to:
        filters["date_to"] = date_to
    if order_by:
        filters["order_by"] = order_by
    
    return crud.get_emissions(db, skip=skip, limit=limit, filters=filters)


@router.get("/emissions/{emission_id}", response_model=schemas.EmissionResponse, tags=["Emissions"])
def get_emission(emission_id: int, db: Session = Depends(get_db)):
    #Récupérer une émission par son ID
    emission = crud.get_emission_by_id(db, emission_id)
    if not emission:
        raise HTTPException(status_code=404, detail="Emission not found")
    return emission


# AIR QUALITY
@router.get("/air-quality", response_model=List[schemas.GlobalResponse], tags=["Air Quality"])
def get_air_quality(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre maximum d'éléments à retourner"),
    city: Optional[str] = Query(None, description="Filtrer par ville"),
    country: Optional[str] = Query(None, description="Filtrer par pays"),
    date_from: Optional[date] = Query(None, description="Date de début (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="Date de fin (YYYY-MM-DD)"),
    order_by: Optional[str] = Query(None, description="Champ de tri (préfixer par '-' pour décroissant)"),
    db: Session = Depends(get_db)
):
    #Récupérer la liste des mesures de qualité d'air avec filtres optionnels
    filters = {}
    if city:
        filters["city"] = city
    if country:
        filters["country"] = country
    if date_from:
        filters["date_from"] = date_from
    if date_to:
        filters["date_to"] = date_to
    if order_by:
        filters["order_by"] = order_by
    
    return crud.get_air_quality(db, skip=skip, limit=limit, filters=filters)


@router.get("/air-quality/{air_quality_id}", response_model=schemas.GlobalResponse, tags=["Air Quality"])
def get_air_quality_item(air_quality_id: int, db: Session = Depends(get_db)):
    #Récupérer une mesure de qualité d'air par son ID
    air_quality = crud.get_air_quality_by_id(db, air_quality_id)
    if not air_quality:
        raise HTTPException(status_code=404, detail="Air quality data not found")
    return air_quality


# SOURCES
@router.get("/sources", response_model=List[schemas.SourceResponse], tags=["Sources"])
def get_sources(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre maximum d'éléments à retourner"),
    db: Session = Depends(get_db)
):
    #Récupérer la liste des sources de données
    return crud.get_sources(db, skip=skip, limit=limit)


@router.get("/sources/{source_id}", response_model=schemas.SourceResponse, tags=["Sources"])
def get_source(source_id: int, db: Session = Depends(get_db)):
    #Récupérer une source par son ID
    source = crud.get_source_by_id(db, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


# USERS
@router.post("/users/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED, tags=["Users"])
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #Inscription d'un nouvel utilisateur
    try:
        return crud.create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/users/login", tags=["Users"])
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):

    #Connexion et génération du token JWT
    user = crud.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    token = jwt.encode(
        {"sub": user.email, "role": user.role, "exp": datetime.utcnow() + timedelta(hours=1)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    return {"access_token": token, "token_type": "bearer"}


@router.get("/users", response_model=List[schemas.UserResponse], tags=["Users"])
def get_users(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre maximum d'éléments à retourner"),
    user=Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    #Récupérer la liste des utilisateurs (admin uniquement)
    return crud.get_users(db, skip=skip, limit=limit)


@router.get("/users/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
def get_user(
    user_id: int,
    user=Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    #Récupérer un utilisateur par son ID (admin uniquement)
    db_user = crud.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(
    user_id: int,
    user=Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    #Supprimer un utilisateur (admin uniquement)
    if not crud.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return None


@router.put("/users/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    user=Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    #Mettre à jour un utilisateur - modification du rôle (admin uniquement)
    try:
        updated_user = crud.update_user(db, user_id, user_update)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# STATISTIQUES
@router.get("/stats/air/averages", tags=["Statistics"])
def get_air_averages(
    date_from: Optional[str] = Query(None, description="Date de début (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Date de fin (YYYY-MM-DD)"),
    zone: Optional[str] = Query(None, description="Pays/Zone"),
    db: Session = Depends(get_db)
):
    #Moyennes des polluants sur une période
    return crud.get_air_quality_averages(db, date_from, date_to, zone)


@router.get("/stats/co2/trend", tags=["Statistics"])
def get_co2_trend(
    zone: Optional[str] = Query(None, description="Pays/Zone"),
    period: str = Query("monthly", regex="^(monthly|yearly)$", description="Période (monthly/yearly)"),
    sector: Optional[str] = Query(None, description="Secteur"),
    db: Session = Depends(get_db)
):
    #Évolution des émissions CO2
    return crud.get_co2_trend(db, zone, period, sector)
