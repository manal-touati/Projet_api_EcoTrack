from sqlalchemy import and_, asc, desc, func
from sqlalchemy.orm import Session
import bcrypt
from datetime import datetime
from app.models import Emission, Global, Source, User
from app.schemas import (
    EmissionCreate, EmissionUpdate,
    GlobalCreate, GlobalUpdate,
    SourceCreate, SourceUpdate,
    UserCreate, UserUpdate
)


# CRUD EMISSIONS
def get_emissions(db: Session, skip: int = 0, limit: int = 100, filters: dict = None):

    #Liste des émissions avec filtres et pagination
    query = db.query(Emission)
    
    if filters:
        if filters.get("country"):
            query = query.filter(Emission.country == filters["country"])
        if filters.get("sector"):
            query = query.filter(Emission.sector == filters["sector"])
        if filters.get("date_from"):
            query = query.filter(Emission.date >= filters["date_from"])
        if filters.get("date_to"):
            query = query.filter(Emission.date <= filters["date_to"])
        
        order = filters.get("order_by")
        if order:
            desc_mode = order.startswith("-")
            field_name = order.lstrip('-')
            if hasattr(Emission, field_name):
                field = getattr(Emission, field_name)
                query = query.order_by(desc(field) if desc_mode else asc(field))
    
    return query.offset(skip).limit(limit).all()


def get_emission_by_id(db: Session, emission_id: int):

    #Récupérer une émission par ID
    return db.query(Emission).filter(Emission.id == emission_id).first()


# CRUD GLOBAL
def get_air_quality(db: Session, skip: int = 0, limit: int = 100, filters: dict = None):

    #Liste des mesures de qualité d'air avec filtres et pagination
    query = db.query(Global)
    
    if filters:
        if filters.get("city"):
            query = query.filter(Global.city.ilike(f"%{filters['city']}%"))
        if filters.get("country"):
            query = query.filter(Global.country == filters["country"])
        if filters.get("date_from"):
            query = query.filter(Global.date >= filters["date_from"])
        if filters.get("date_to"):
            query = query.filter(Global.date <= filters["date_to"])
        
        order = filters.get("order_by")
        if order:
            desc_mode = order.startswith("-")
            field_name = order.lstrip('-')
            if hasattr(Global, field_name):
                field = getattr(Global, field_name)
                query = query.order_by(desc(field) if desc_mode else asc(field))
    
    return query.offset(skip).limit(limit).all()


def get_air_quality_by_id(db: Session, air_quality_id: int):

    #Récupérer une mesure par ID
    return db.query(Global).filter(Global.id == air_quality_id).first()


# CRUD SOURCES
def get_sources(db: Session, skip: int = 0, limit: int = 100):

    #Liste des sources avec pagination
    return db.query(Source).offset(skip).limit(limit).all()


def get_source_by_id(db: Session, source_id: int):

    #Récupérer une source par ID
    return db.query(Source).filter(Source.id == source_id).first()


# CRUD USERS
def get_users(db: Session, skip: int = 0, limit: int = 100):

    #Liste des utilisateurs avec pagination
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):

    #Récupérer un utilisateur par ID
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):

    #Récupérer un utilisateur par email
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):

    #Récupérer un utilisateur par username
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):

    #Créer un nouvel utilisateur avec mot de passe haché
    if get_user_by_email(db, user.email):
        raise ValueError("Un utilisateur avec cet email existe déjà")
    if get_user_by_username(db, user.username):
        raise ValueError("Un utilisateur avec ce username existe déjà")
    
    hashed_password = bcrypt.hashpw(user.password[:72].encode('utf-8'), bcrypt.gensalt())
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password.decode('utf-8'),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password: str, hashed_password: str):

    #Vérifier le mot de passe
    return bcrypt.checkpw(plain_password[:72].encode('utf-8'), hashed_password.encode('utf-8'))


def authenticate_user(db: Session, email: str, password: str):

    #Authentifier un utilisateur
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def delete_user(db: Session, user_id: int):

    #Supprimer un utilisateur
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


def update_user(db: Session, user_id: int, user_update: UserUpdate):

    #Mettre à jour un utilisateur (rôle, etc.)
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    if user_update.username is not None:
        existing = get_user_by_username(db, user_update.username)
        if existing and existing.id != user_id:
            raise ValueError("Un utilisateur avec ce username existe déjà")
        user.username = user_update.username
    
    if user_update.email is not None:
        existing = get_user_by_email(db, user_update.email)
        if existing and existing.id != user_id:
            raise ValueError("Un utilisateur avec cet email existe déjà")
        user.email = user_update.email
    
    if user_update.password is not None:
        hashed_password = bcrypt.hashpw(user_update.password[:72].encode('utf-8'), bcrypt.gensalt())
        user.password = hashed_password.decode('utf-8')
    
    if user_update.role is not None:
        user.role = user_update.role
    
    db.commit()
    db.refresh(user)
    return user


# STATISTIQUES
def get_air_quality_averages(db: Session, date_from: str = None, date_to: str = None, zone: str = None):

    #Calculer les moyennes des polluants sur une période
    query = db.query(
        func.avg(Global.pm25).label('pm25_avg'),
        func.avg(Global.pm10).label('pm10_avg'),
        func.avg(Global.no2).label('no2_avg'),
        func.avg(Global.so2).label('so2_avg'),
        func.avg(Global.co).label('co_avg'),
        func.avg(Global.o3).label('o3_avg')
    )
    
    if date_from:
        from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
        query = query.filter(Global.date >= from_date)
    if date_to:
        to_date = datetime.strptime(date_to, '%Y-%m-%d').date()
        query = query.filter(Global.date <= to_date)
    if zone:
        query = query.filter(Global.country == zone)
    
    result = query.first()
    
    return {
        "pm25_avg": round(float(result.pm25_avg), 2) if result and result.pm25_avg is not None else 0,
        "pm10_avg": round(float(result.pm10_avg), 2) if result and result.pm10_avg is not None else 0,
        "no2_avg": round(float(result.no2_avg), 2) if result and result.no2_avg is not None else 0,
        "so2_avg": round(float(result.so2_avg), 2) if result and result.so2_avg is not None else 0,
        "co_avg": round(float(result.co_avg), 2) if result and result.co_avg is not None else 0,
        "o3_avg": round(float(result.o3_avg), 2) if result and result.o3_avg is not None else 0
    }


def get_co2_trend(db: Session, zone: str = None, period: str = "monthly", sector: str = None):

    #Obtenir l'évolution des émissions CO2
    if period == "monthly":
        date_format = func.strftime('%Y-%m', Emission.date)
    else:
        date_format = func.strftime('%Y', Emission.date)
    
    query = db.query(
        date_format.label('period'),
        func.sum(Emission.value).label('total')
    )
    
    if zone:
        query = query.filter(Emission.country == zone)
    if sector:
        query = query.filter(Emission.sector == sector)
    
    query = query.group_by('period').order_by('period')
    
    results = query.all()
    
    return {
        "labels": [r.period for r in results],
        "values": [round(r.total, 2) for r in results]
    }
