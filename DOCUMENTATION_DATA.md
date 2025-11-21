# Documentation des Sources de Données - EcoTrack

## Sources de Données Utilisées

### 1. Émissions de CO2 par Secteur
**Fichier:** `data/co2_emissions_by_sector.csv`

**Description:**
Dataset global contenant les émissions de dioxyde de carbone (CO2) par pays et par secteur d'activité économique.

**Colonnes:**
- `country`: Nom du pays ou région
- `sector`: Secteur d'activité (Power, Industry, Transport, Residential, Commercial, Agriculture)
- `date`: Date de la mesure
- `value`: Émission en mégatonnes de CO2 (Mt CO2)

**Source:**
- Type: Données environnementales globales
- Origine: Organisations internationales (IEA, World Bank, EPA)
- URL de référence: https://www.kaggle.com/datasets/emissions-co2-sector

**Justification du choix:**
- **Pertinence:** Les émissions de CO2 sont un indicateur clé du changement climatique et de l'impact environnemental des activités humaines
- **Granularité:** La segmentation par secteur permet d'identifier les sources principales d'émissions et de cibler les actions de réduction
- **Couverture:** Données mondiales permettant des comparaisons entre pays et régions
- **Temporalité:** Historique permettant d'analyser les tendances et l'évolution des émissions
- **Utilité pour l'API:** Permet de répondre aux questions sur les émissions par pays, secteur et période

**Nombre d'enregistrements:** ~135,000

---

### 2. Qualité de l'Air Globale
**Fichier:** `data/global_air_quality.csv`

**Description:**
Base de données mondiale de la qualité de l'air mesurée dans différentes villes, incluant les principaux polluants atmosphériques.

**Colonnes:**
- `city`: Nom de la ville
- `country`: Pays
- `date`: Date de la mesure
- `pm25`: Particules fines PM2.5 (µg/m³) - particules de diamètre < 2.5 microns
- `pm10`: Particules PM10 (µg/m³) - particules de diamètre < 10 microns
- `no2`: Dioxyde d'azote (µg/m³)
- `so2`: Dioxyde de soufre (µg/m³)
- `co`: Monoxyde de carbone (mg/m³)
- `o3`: Ozone (µg/m³)

**Source:**
- Type: Données de santé environnementale
- Origine: Organisation Mondiale de la Santé (WHO), stations de surveillance locales
- URL de référence: https://www.who.int/data/gho/data/themes/air-pollution

**Justification du choix:**
- **Impact sanitaire:** La qualité de l'air a un impact direct sur la santé publique (maladies respiratoires, cardiovasculaires)
- **Indicateurs standardisés:** Les polluants mesurés sont reconnus internationalement par l'OMS
- **Données urbaines:** Focus sur les villes où vit la majorité de la population mondiale
- **Complémentarité:** Complète les données CO2 avec des indicateurs de pollution locale
- **Utilité pour l'API:** Permet de surveiller et comparer la qualité de l'air entre villes et pays

**Nombre d'enregistrements:** ~5,800

---

## Méthodologie de Collecte

### Nettoyage et Préparation
Les données brutes ont été :
1. Vérifiées pour la cohérence des valeurs (pas de valeurs négatives, format de dates)
2. Converties au format CSV standardisé
3. Encodées en UTF-8
4. Validées avec pandas avant insertion en base

### Format de Stockage
- **Base de données:** SQLite (ecotrack.db)
- **ORM:** SQLAlchemy pour la gestion des modèles
- **Indexation:** Index sur les colonnes country, date, city pour optimiser les requêtes

---

## Limitations et Considérations

### Émissions CO2
- Les données représentent des estimations basées sur les rapports nationaux
- Certains pays peuvent avoir des données manquantes pour certaines années
- Les méthodologies de calcul peuvent varier selon les pays

### Qualité de l'Air
- La couverture géographique est inégale (plus de stations dans les pays développés)
- Les mesures peuvent varier selon les conditions météorologiques
- Certaines villes ont des données plus complètes que d'autres

---

## Utilisation dans l'API

Ces données alimentent les endpoints suivants :

**Émissions CO2:**
- `GET /emissions` - Liste paginée avec filtres
- `GET /emissions/{id}` - Détail d'une mesure
- `GET /stats/co2/trend` - Tendances temporelles

**Qualité de l'Air:**
- `GET /air-quality` - Liste paginée avec filtres
- `GET /air-quality/{id}` - Détail d'une mesure
- `GET /stats/air/averages` - Moyennes des polluants

**Métadonnées:**
- `GET /sources` - Liste des sources de données

---

## Mises à Jour

**Fréquence recommandée:**
- Émissions CO2: Annuelle (nouvelles données publiées chaque année)
- Qualité de l'air: Mensuelle ou trimestrielle (données plus fréquentes)

**Procédure:**
1. Télécharger les nouvelles données depuis les sources
2. Vérifier le format et la cohérence
3. Exécuter le script `init_db.py` pour recharger la base

Dernière mise à jour: Novembre 2025
