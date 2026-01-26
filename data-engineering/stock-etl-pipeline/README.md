<h1 align="center">Stock ETL Pipeline</h1>

## Objectif du projet
Ce projet illustre la mise en place d’un **pipeline ETL (Extract, Transform, Load)** permettant de :
- collecter des données financières (actions boursières),
- les nettoyer et structurer,
- puis les charger dans une base de données **PostgreSQL**.

L’objectif est de démontrer des **bonnes pratiques de Data Engineering** applicables en environnement professionnel : modularité, idempotence, gestion des erreurs et clarté du code.

---

## Architecture du projet

```text
data-engineering/
└── stock-etl-pipeline/
    ├── src/
    │   ├── create_table.py     # Création de la base de données
    │   ├── db.py               # Configuration et liaison avec la base de données
    │   ├── extract.py          # Extraction des données (API / fichiers)
    │   ├── transform.py        # Nettoyage et transformation des données
    │   ├── load.py             # Chargement dans PostgreSQL
    │   └── main.py             # Le fichier principal pour faire marcher tous les codes
    │
    ├── data/
    │   └── raw/            # Données brutes (CSV)
    │
    ├── requirements.txt   # Dépendances Python
    └── README.md
