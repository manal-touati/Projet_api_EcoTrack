# EcoTrack - API de Suivi Environnemental

API REST développée avec FastAPI pour le suivi des émissions de CO2 et de la qualité de l'air à l'échelle mondiale.

## Description du Projet

EcoTrack est une API qui permet de :
- Consulter les émissions de CO2 par pays et secteur d'activité
- Suivre la qualité de l'air dans différentes villes du monde
- Analyser les tendances et calculer des statistiques environnementales
- Gérer les utilisateurs avec authentification JWT

Le projet inclut un dashboard web interactif pour visualiser et filtrer les données en temps réel.

## Installation

### Prérequis
- Python 3.8+
- pip

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/manal-touati/Projet_api_EcoTrack.git
cd Projet_api_EcoTrack
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Initialiser la base de données**
```bash
python init_db.py
```
Ce script va :
- Créer la base de données SQLite (`ecotrack.db`)
- Charger les données depuis les fichiers CSV
- Créer les utilisateurs par défaut

**Utilisateurs créés automatiquement:**
- Admin: `admin@ecotrack.com` / `admin123`
- User: `user@ecotrack.com` / `user123`

## Utilisation

### Lancer l'API

```bash
uvicorn app.main:app --reload
```

L'API sera accessible sur : `http://127.0.0.1:8000`

### Accéder au Dashboard

Une fois l'API lancée, ouvrez votre navigateur et accédez à :
- **Dashboard**: http://127.0.0.1:8000/dashboard
- **Documentation Swagger**: http://127.0.0.1:8000/docs
- **Documentation ReDoc**: http://127.0.0.1:8000/redoc

## Endpoints Disponibles

### Émissions CO2

| Méthode | Endpoint | Description | Authentification |
|---------|----------|-------------|------------------|
| GET | `/emissions` | Liste paginée des émissions avec filtres (pays, secteur, dates) | Non |
| GET | `/emissions/{id}` | Détail d'une émission spécifique | Non |

**Filtres disponibles:**
- `country`: Filtrer par pays
- `sector`: Filtrer par secteur (Power, Industry, Transport, etc.)
- `date_from` / `date_to`: Filtrer par période
- `skip` / `limit`: Pagination

### Qualité de l'Air

| Méthode | Endpoint | Description | Authentification |
|---------|----------|-------------|------------------|
| GET | `/air-quality` | Liste paginée des mesures avec filtres (ville, pays, dates) | Non |
| GET | `/air-quality/{id}` | Détail d'une mesure spécifique | Non |

**Filtres disponibles:**
- `city`: Filtrer par ville
- `country`: Filtrer par pays
- `date_from` / `date_to`: Filtrer par période
- `skip` / `limit`: Pagination

### Statistiques

| Méthode | Endpoint | Description | Authentification |
|---------|----------|-------------|------------------|
| GET | `/stats/air/averages` | Moyennes des polluants atmosphériques | Non |
| GET | `/stats/co2/trend` | Tendances des émissions CO2 par période | Non |

**Paramètres stats air:**
- `date_from` / `date_to`: Période d'analyse
- `zone`: Filtrer par zone géographique

**Paramètres stats CO2:**
- `period`: `monthly` ou `yearly`
- `zone`: Filtrer par zone géographique

### Utilisateurs

| Méthode | Endpoint | Description | Authentification |
|---------|----------|-------------|------------------|
| POST | `/users/register` | Créer un nouvel utilisateur | Non |
| POST | `/users/login` | Se connecter et obtenir un token JWT | Non |
| GET | `/users` | Liste des utilisateurs | Admin |
| GET | `/users/{id}` | Détail d'un utilisateur | Admin |
| DELETE | `/users/{id}` | Supprimer un utilisateur | Admin |

### Sources de Données

| Méthode | Endpoint | Description | Authentification |
|---------|----------|-------------|------------------|
| GET | `/sources` | Liste des sources de données utilisées | Non |
| GET | `/sources/{id}` | Détail d'une source | Non |

## Authentification

L'API utilise JWT (JSON Web Tokens) pour l'authentification.

**Pour obtenir un token:**
```http
POST /users/login
Content-Type: application/json

{
  "email": "admin@ecotrack.com",
  "password": "admin123"
}
```

**Utiliser le token:**
```http
GET /users
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Structure du Projet

```
Projet_api_EcoTrack/
├── app/
│   ├── __init__.py
│   ├── main.py          # Point d'entrée FastAPI
│   ├── models.py        # Modèles SQLAlchemy
│   ├── schemas.py       # Schémas Pydantic
│   ├── database.py      # Configuration BDD
│   ├── crud.py          # Opérations CRUD
│   └── routes.py        # Endpoints de l'API
├── data/
│   ├── co2_emissions_by_sector.csv
│   └── global_air_quality.csv
├── frontend/
│   └── index.html       # Dashboard web
├── init_db.py           # Script d'initialisation BDD
├── requirements.txt     # Dépendances Python
├── README.md
├── DOCUMENTATION_DATA.md # Documentation des sources
└── ecotrack.db         # Base de données SQLite

```

## Sources de Données

### 1. Émissions de CO2 par Secteur
- **Format**: CSV (~135,000 enregistrements)
- **Colonnes**: country, sector, date, value (Mt CO2)
- **Source**: Données environnementales globales (IEA, World Bank)
- **Secteurs**: Power, Industry, Transport, Residential, Commercial, Agriculture

### 2. Qualité de l'Air Globale
- **Format**: CSV (~5,800 enregistrements)
- **Colonnes**: city, country, date, pm25, pm10, no2, so2, co, o3
- **Source**: WHO - Organisation Mondiale de la Santé
- **Polluants mesurés**: PM2.5, PM10, NO2, SO2, CO, O3

Pour plus de détails, consultez [DOCUMENTATION_DATA.md](DOCUMENTATION_DATA.md)

## Technologies Utilisées

- **Framework**: FastAPI
- **Base de données**: SQLite
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Authentification**: JWT (python-jose)
- **Sécurité**: bcrypt
- **Frontend**: HTML/CSS/JavaScript + Chart.js
- **Data Processing**: pandas

## Dashboard Web

Le dashboard permet de :
- Se connecter et créer des utilisateurs
- Visualiser les émissions CO2 et qualité de l'air avec filtres
- Afficher des statistiques avec graphiques (camembert, courbes)
- Gérer les utilisateurs (liste, création)
- Interface responsive et moderne

**Fonctionnalités:**
- Tableaux scrollables avec pagination
- Filtres par pays, secteur, ville, période
- Graphiques interactifs (Chart.js)
- Gestion des erreurs
- Authentification JWT stockée en localStorage

## Tests

Pour tester l'API manuellement :
1. Accédez à http://127.0.0.1:8000/docs
2. Utilisez l'interface Swagger pour tester les endpoints
3. Pour les endpoints protégés, utilisez le bouton "Authorize" avec votre token

## Livrables

- **Dépôt Git**: Repository GitHub complet avec code, scripts et documentation
- **Documentation data**: Fichier DOCUMENTATION_DATA.md avec sources et justifications
- **Script d'initialisation**: init_db.py pour charger les données de test
- **Mini dashboard**: Interface web HTML/CSS/JS consommant l'API

## Auteur

Manal Touati - [GitHub](https://github.com/manal-touati)

## Licence

Ce projet est développé dans le cadre d'un projet académique M1 Data Engineering.

---

**EcoTrack - Suivre l'environnement pour un avenir durable**
