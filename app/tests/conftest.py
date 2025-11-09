# app/tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base

# ---- IMPORTER TOUS LES MODELES POUR QUE SQLALCHEMY LES CONNAISSE ----
import app.models.users
import app.models.contracts
import app.models.events
import app.models.clients

# Base en mémoire pour les tests
FAKE_DATA_BASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(FAKE_DATA_BASE_URL, echo=False)
    # Crée toutes les tables en mémoire
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture(scope="function")
def db_session(engine):
    # Réinitialise la base avant chaque test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    SessionTesting = sessionmaker(bind=engine)
    session = SessionTesting()
    yield session
    session.close()
