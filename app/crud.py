from sqlalchemy import and_, asc, desc, func
from sqlalchemy.orm import Session
from app.models import Emission, Global, Source, User
from app.schemas import (
    EmissionCreate, EmissionUpdate,
    GlobalCreate, GlobalUpdate,
    SourceCreate, SourceUpdate,
    UserCreate, UserUpdate
)


# ==================== EMISSIONS CO2 ====================

def get_emissions(db: Session, skip: int = 0, limit: int = 100, filters: dict = None):
    """Liste des émissions avec filtres et pagination"""
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
    """Récupérer une émission par ID"""
    return db.query(Emission).filter(Emission.id == emission_id).first()


def create_emission(db: Session, emission: EmissionCreate):
    """Créer une nouvelle émission"""
    existing = db.query(Emission).filter(
        and_(
            Emission.country == emission.country,
            Emission.date == emission.date,
            Emission.sector == emission.sector
        )
    ).first()
    
    if existing:
        raise ValueError("Une émission pour ce pays, date et secteur existe déjà")
    
    db_emission = Emission(**emission.model_dump())
    db.add(db_emission)
    db.commit()
    db.refresh(db_emission)
    return db_emission


def update_emission(db: Session, emission_id: int, emission: EmissionUpdate):
    """Mettre à jour une émission"""
    db_emission = db.query(Emission).filter(Emission.id == emission_id).first()
    if not db_emission:
        return None
    
    update_data = emission.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_emission, field, value)
    
    db.commit()
    db.refresh(db_emission)
    return db_emission


def delete_emission(db: Session, emission_id: int):
    """Supprimer une émission"""
    db_emission = db.query(Emission).filter(Emission.id == emission_id).first()
    if not db_emission:
        return False
    
    db.delete(db_emission)
    db.commit()
    return True


# ==================== GLOBAL AIR QUALITY ====================

def get_air_quality(db: Session, skip: int = 0, limit: int = 100, filters: dict = None):
    """Liste des mesures de qualité d'air avec filtres et pagination"""
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
    """Récupérer une mesure par ID"""
    return db.query(Global).filter(Global.id == air_quality_id).first()


def create_air_quality(db: Session, air_quality: GlobalCreate):
    """Créer une nouvelle mesure de qualité d'air"""
    existing = db.query(Global).filter(
        and_(
            Global.city == air_quality.city,
            Global.country == air_quality.country,
            Global.date == air_quality.date
        )
    ).first()
    
    if existing:
        raise ValueError("Une mesure pour cette ville, pays et date existe déjà")
    
    db_air_quality = Global(**air_quality.model_dump())
    db.add(db_air_quality)
    db.commit()
    db.refresh(db_air_quality)
    return db_air_quality


def update_air_quality(db: Session, air_quality_id: int, air_quality: GlobalUpdate):
    """Mettre à jour une mesure de qualité d'air"""
    db_air_quality = db.query(Global).filter(Global.id == air_quality_id).first()
    if not db_air_quality:
        return None
    
    update_data = air_quality.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_air_quality, field, value)
    
    db.commit()
    db.refresh(db_air_quality)
    return db_air_quality


def delete_air_quality(db: Session, air_quality_id: int):
    """Supprimer une mesure de qualité d'air"""
    db_air_quality = db.query(Global).filter(Global.id == air_quality_id).first()
    if not db_air_quality:
        return False
    
    db.delete(db_air_quality)
    db.commit()
    return True


# ==================== SOURCES ====================

def get_sources(db: Session, skip: int = 0, limit: int = 100):
    """Liste des sources avec pagination"""
    return db.query(Source).offset(skip).limit(limit).all()


def get_source_by_id(db: Session, source_id: int):
    """Récupérer une source par ID"""
    return db.query(Source).filter(Source.id == source_id).first()


def create_source(db: Session, source: SourceCreate):
    """Créer une nouvelle source"""
    existing = db.query(Source).filter(Source.name == source.name).first()
    if existing:
        raise ValueError("Une source avec ce nom existe déjà")
    
    db_source = Source(**source.model_dump())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


def update_source(db: Session, source_id: int, source: SourceUpdate):
    """Mettre à jour une source"""
    db_source = db.query(Source).filter(Source.id == source_id).first()
    if not db_source:
        return None
    
    update_data = source.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_source, field, value)
    
    db.commit()
    db.refresh(db_source)
    return db_source


def delete_source(db: Session, source_id: int):
    """Supprimer une source"""
    db_source = db.query(Source).filter(Source.id == source_id).first()
    if not db_source:
        return False
    
    db.delete(db_source)
    db.commit()
    return True


# ==================== USERS ====================

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Liste des utilisateurs avec pagination"""
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    """Récupérer un utilisateur par ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """Récupérer un utilisateur par email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    """Récupérer un utilisateur par username"""
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    """Créer un nouveau utilisateur"""
    if get_user_by_email(db, user.email):
        raise ValueError("Un utilisateur avec cet email existe déjà")
    if get_user_by_username(db, user.username):
        raise ValueError("Un utilisateur avec ce username existe déjà")
    
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: UserUpdate):
    """Mettre à jour un utilisateur"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    update_data = user.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    """Supprimer un utilisateur"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True
