from app.models.users import Collaborateur, Role
from app.security.permission import require_role, require_auth
from app.sentry.decorateur_sentry import sentry_wrap
from app.db.base import SessionLocal

from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

@sentry_wrap
def get_all_collaborateurs(current_user):
    with SessionLocal() as session:
        collaborateurs = session.query(Collaborateur).options(
            joinedload(Collaborateur.role)
        ).all()
        return collaborateurs

@sentry_wrap  
def get_collaborateur_by_id(collaborateur_id):
    with SessionLocal() as session:
        collaborateur = session.query(Collaborateur).options(
            joinedload(Collaborateur.role),
            joinedload(Collaborateur.contracts)
        ).filter_by(id=collaborateur_id).first()
        if not collaborateur:
            raise ValueError("Aucun collaborateur avec cet id.")
        return collaborateur
    
def get_role_by_name(role_name):
    with SessionLocal() as session:
        role = session.query(Role).filter_by(nom=role_name).first()
        return role

@sentry_wrap    
def get_all_commercials(current_user):
    with SessionLocal() as session:
        commercial_team = session.query(Collaborateur).filter(Collaborateur.role=='commercial').all()
        return commercial_team

@sentry_wrap    
def get_support_team(current_user):
    with SessionLocal() as session:
        support_team = session.query(Collaborateur).filter(Collaborateur.role=='support').all()
        return support_team

@sentry_wrap   
def get_support_by_id(current_user, collaborateur_id):
    support_team = get_support_team(current_user)
    with SessionLocal() as session:
        support = session.query(Collaborateur).filter_by(id=collaborateur_id).first()
        if support not in support_team: 
            raise ValueError("Ce collaborateur ne fait pas partie de l'équipe de support.")
        return support 

@sentry_wrap
def get_commercial_by_fullname(current_user, fullname):
    with SessionLocal() as session:
        commercial = (
            session.query(Collaborateur)
            .filter(Collaborateur.role.has(nom="commercial"), Collaborateur.nom == fullname)
            .first()
        )
        if not commercial:
            raise ValueError("Aucun commercial de ce nom n'a été trouvé.")
        return commercial 


@sentry_wrap
def create_collaborateur(current_user, nom, prenom, email, departement, role, password):
    with SessionLocal() as session:
        data = [nom, prenom, email, departement, role]
        if not all(data):
            raise ValueError("Tous les champs sont obligatoires.")
        
        existing = session.query(Collaborateur).filter_by(email=email).first()
        if existing:
            raise ValueError("Ce collaborateur existe déjà.")
        
        role_obj = session.query(Role).filter_by(nom=role).first()
        if not role_obj:
            raise ValueError("Le rôle spécifié n'existe pas (choisissez parmi : commercial, gestion, support).")
        
        hashed_pw = generate_password_hash(password)
        
        new_collaborateur = Collaborateur(
            nom=nom,
            prenom=prenom,
            email=email,
            departement=departement,
            role_id=role_obj.id,
            password_hash=hashed_pw
        )

        session.add(new_collaborateur)
        session.commit()
        session.refresh(new_collaborateur)

        return new_collaborateur


@sentry_wrap
def update_collaborateur(collaborator_id, **updates):
    with SessionLocal() as session:
        collaborator = session.query(Collaborateur).filter_by(id=collaborator_id).first()

        if not collaborator:
            raise ValueError("Aucun collaborateur trouvé.")

       # --- Gestion des relations (ex: ajout de contrat) ---
        add_contract = updates.pop("add_contract", None)
        if add_contract is not None:  # add_contract doit être un objet Contract
            collaborator.contracts.append(add_contract)

        # --- Mise à jour des champs ---
        for key, value in updates.items():
            if hasattr(collaborator, key) and value is not None:
                setattr(collaborator, key, value)

        session.commit()
        session.refresh(collaborator)

        return collaborator


@sentry_wrap
def delete_collaborateur(current_user, collaborateur_id):
    with SessionLocal() as session:
        collaborateur = session.query(Collaborateur).filter_by(id=collaborateur_id).first()
        
        if not collaborateur:
            raise ValueError(f"Aucun collaborateur trouvé avec l'id {collaborateur_id}.")
        
        try:
            session.delete(collaborateur)
            session.commit()
            return f"Collaborateur {collaborateur.prenom} {collaborateur.nom} supprimé avec succès."
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Erreur lors de la suppression : {e}")
