from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Chaîne de connexion à la base
DATABASE_URL = "postgresql+psycopg2://crm_user:crm_password@localhost:5432/epic_events_crm"

# Création de l'engine
engine = create_engine(DATABASE_URL, echo=False)  # echo=True permet de voir les requêtes SQL dans le terminal

# Création de la classe Base pour tous les modèles
Base = declarative_base()

# Création de la session pour interagir avec la BDD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
