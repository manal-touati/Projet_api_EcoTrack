from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date as date_type, datetime
from typing import Optional


# Schémas pour les émissions CO2
class EmissionBase(BaseModel):
    country: str = Field(..., min_length=2, max_length=100)
    date: date_type
    sector: str = Field(..., min_length=2)
    value: float = Field(..., ge=0)
    timestamp: int = Field(..., ge=0)
    source_id: Optional[int] = None

    @field_validator('sector')
    def sector_must_be_valid(cls, v):
        allowed_sectors = ["Power", "Industry", "Transport", "Residential", "Commercial", "Agriculture"]
        if v not in allowed_sectors:
            raise ValueError(f'Sector must be one of: {", ".join(allowed_sectors)}')
        return v


class EmissionCreate(EmissionBase):
    pass


class EmissionUpdate(BaseModel):
    country: Optional[str] = Field(None, min_length=2, max_length=100)
    date: Optional[date_type] = None
    sector: Optional[str] = Field(None, min_length=2)
    value: Optional[float] = Field(None, ge=0)
    timestamp: Optional[int] = Field(None, ge=0)
    source_id: Optional[int] = None

    @field_validator('sector')
    def sector_must_be_valid(cls, v):
        if v is not None:
            allowed_sectors = ["Power", "Industry", "Transport", "Residential", "Commercial", "Agriculture"]
            if v not in allowed_sectors:
                raise ValueError(f'Sector must be one of: {", ".join(allowed_sectors)}')
        return v


class EmissionResponse(EmissionBase):
    id: int

    class Config:
        from_attributes = True


# Schémas pour la qualité de l'air globale
class GlobalBase(BaseModel):
    city: str = Field(..., min_length=2, max_length=100)
    country: str = Field(..., min_length=2, max_length=100)
    date: date_type
    pm25: float = Field(..., ge=0, le=500)
    pm10: float = Field(..., ge=0, le=600)
    no2: float = Field(..., ge=0, le=200)
    so2: float = Field(..., ge=0, le=200)
    co: float = Field(..., ge=0, le=50)
    o3: float = Field(..., ge=0, le=300)
    temperature: float = Field(..., ge=-50, le=60)
    humidity: float = Field(..., ge=0, le=100)
    wind_speed: float = Field(..., ge=0, le=100)
    source_id: Optional[int] = None


class GlobalCreate(GlobalBase):
    pass


class GlobalUpdate(BaseModel):
    city: Optional[str] = Field(None, min_length=2, max_length=100)
    country: Optional[str] = Field(None, min_length=2, max_length=100)
    date: Optional[date_type] = None
    pm25: Optional[float] = Field(None, ge=0, le=500)
    pm10: Optional[float] = Field(None, ge=0, le=600)
    no2: Optional[float] = Field(None, ge=0, le=200)
    so2: Optional[float] = Field(None, ge=0, le=200)
    co: Optional[float] = Field(None, ge=0, le=50)
    o3: Optional[float] = Field(None, ge=0, le=300)
    temperature: Optional[float] = Field(None, ge=-50, le=60)
    humidity: Optional[float] = Field(None, ge=0, le=100)
    wind_speed: Optional[float] = Field(None, ge=0, le=100)
    source_id: Optional[int] = None


class GlobalResponse(GlobalBase):
    id: int

    class Config:
        from_attributes = True


# Schémas pour les utilisateurs
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: str = Field(default='user')

    @field_validator('role')
    def role_must_be_valid(cls, v):
        allowed_roles = ['user', 'admin']
        if v not in allowed_roles:
            raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None

    @field_validator('role')
    def role_must_be_valid(cls, v):
        if v is not None:
            allowed_roles = ['user', 'admin']
            if v not in allowed_roles:
                raise ValueError(f'Role must be one of: {", ".join(allowed_roles)}')
        return v


class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


# Schémas pour les sources
class SourceBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    origin: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = Field(None, max_length=500)


class SourceCreate(SourceBase):
    pass


class SourceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    origin: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = Field(None, max_length=500)


class SourceResponse(SourceBase):
    id: int

    class Config:
        from_attributes = True


# Schémas pour l'authentification
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
