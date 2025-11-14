from app.db.base import SessionLocal
from app.models.clients import Client
from app.models.contracts import Contract
from app.models.events import Event
from app.models.users import Collaborateur
from app.security.permission import require_auth, require_role
from app.sentry.decorateur_sentry import sentry_wrap

from datetime import datetime

@sentry_wrap
def get_all_clients(current_user):
    with SessionLocal() as session:
        clients = session.query(Client).all()
        return clients
@sentry_wrap
def get_client_by_id(client_id):
    with SessionLocal() as session:
        client = session.query(Client).filter(Client.id==client_id).first()
        if not client:
            raise ValueError(f"Aucun client trouvé pour l'identifiant {client_id}.")
        return client 

@sentry_wrap
def get_client_by_fullname(current_user, fullname): 
    with SessionLocal() as session:
        client = session.query(Client).filter_by(fullname=fullname).first()
        if not client:
            raise ValueError("Auncun client de ce nom n'a été trouvé.")
        return client 

@sentry_wrap
def create_client(current_user, fullname, email, telephone, entreprise, commercial_id, contract_id=None, event_id=None):
    with SessionLocal() as session: 
        data = [fullname, email, telephone, entreprise, commercial_id]
        if not all(data):
            raise ValueError("Les champs suivant sont obligatoire : fullname, email, telephone, entreprise, commercial_id")
        
        commercial = session.query(Collaborateur).filter_by(id=commercial_id).first()
        if not commercial:
            raise ValueError("Aucun collaborateur trouvé avec cet id.")

        new_client = Client(
            fullname=fullname, 
            email=email,
            telephone=telephone,
            entreprise=entreprise,
            commercial_id=commercial_id,
        )

        if contract_id:
            contract = session.query(Contract).filter_by(id=contract_id).first()
            if not contract: 
                raise ValueError("Aucun contrat trouvé avec cet id.")
            new_client.contracts.append(contract)

        if event_id:
            event = session.query(Event).filter_by(id=event_id).first()
            if not event:
                raise ValueError("Aucun event trouvé avec cet id.")
            new_client.events.append(event)

        session.add(new_client)
        session.commit()
        session.refresh(new_client)

        return new_client

@sentry_wrap
def update_client(current_user, client_id, **updates):
    with SessionLocal() as session:
        client = session.query(Client).filter_by(id=client_id).first()
        if not client:
            raise ValueError("Ce client n'existe pas.")
        
        if client.commercial_id != current_user.id:
            raise ValueError("Vous ne pouvez pas modifier les informations d’un client qui ne vous appartient pas.")
        
        for key, value in updates.items():
            if hasattr(client, key):
                setattr(client, key, value)

        client.date_updated = datetime.now().isoformat()

        session.commit()
        session.refresh(client)
        return client
    