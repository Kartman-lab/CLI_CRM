import jwt
import datetime
import os
import json
from sqlalchemy.orm import joinedload
from pathlib import Path
from dotenv import load_dotenv
from app.db.base import SessionLocal
from app.models.users import Collaborateur

# Fichier pour stocker la session localement
SESSION_FILE = Path.home() / "epic_events_session.json"

load_dotenv()
secret_key = os.getenv("JWT_SECRET")


# --- Authentification de l'utilisateur ---
def authenticate_user(email: str, password: str):
    session = SessionLocal()
    user = session.query(Collaborateur).filter(Collaborateur.email == email).first()
    if user and user.check_password(password):
        return user
    return None


# --- Création du token JWT ---
def create_access_token(user: Collaborateur):
    payload = {
        "sub": user.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token  


# --- Décodage du token et récupération de l'utilisateur ---
def get_user_from_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        with SessionLocal() as session:
            user = (
                session.query(Collaborateur)
                .options(joinedload(Collaborateur.role))
                .filter(Collaborateur.email == payload["sub"])
                .first()
            )
            return user
    except jwt.ExpiredSignatureError:
        print("Le token a expiré, veuillez vous reconnecter.")
        return None
    except jwt.DecodeError:
        print("Token invalide.")
        return None


# --- Sauvegarde et lecture de la session ---
def save_session(token: str):
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump({"token": token}, f)

def load_session():
    if not SESSION_FILE.exists():
        return None
    with open(SESSION_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("token")

def clear_session():
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()


# --- Fonction de connexion utilisateur ---
def login_user(email, password):
    user = authenticate_user(email, password)
    if user:
        token = create_access_token(user)
        save_session(token)
        return user
    return None
