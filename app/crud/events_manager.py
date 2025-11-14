from sqlalchemy.orm import joinedload

from app.db.base import SessionLocal
from app.models.events import Event
from app.models.users import Collaborateur, Role
from app.models.contracts import Contract
from app.security.permission import require_auth, require_role
from app.sentry.decorateur_sentry import sentry_wrap


@sentry_wrap
def get_all_events(current_user):
    with SessionLocal() as session:
        events = session.query(Event).options(
            joinedload(Event.contract),
            joinedload(Event.client),
            joinedload(Event.support_contact)
        ).all()
        return events

@sentry_wrap
def get_event_by_id(event_id): 
    with SessionLocal() as session:
        event = session.query(Event).filter_by(id=event_id).first()
        if not event:
            raise ValueError("Aucun évènement n'a été trouvé.")
        return event

@sentry_wrap
def get_events_without_support(current_user):
    with SessionLocal() as session:
        events = session.query(Event).filter(Event.support_contact_id.is_(None)).all()
        return events


@sentry_wrap
def get_my_events(current_user):
    with SessionLocal() as session:
        my_events = session.query(Event).options(
            joinedload(Event.contract),
            joinedload(Event.client),
            joinedload(Event.support_contact)
        ).filter(Event.support_contact_id == current_user.id).all()
        return my_events


@sentry_wrap   
def assign_event_support(current_user, event_id, collaborateur_id): 
    with SessionLocal() as session: 
        event = session.query(Event).filter_by(id=event_id).first()
        if not event:
            raise ValueError("Aucun évènement trouvé.")
        if event.support_contact_id is not None: 
            raise ValueError("Cet évènement a déjà un support associé.")

        support = (
            session.query(Collaborateur)
            .join(Collaborateur.role)
            .filter(
                Collaborateur.id == int(collaborateur_id),
                Role.nom == "support" 
            )
            .first()
        )

        if not support:
            raise ValueError("Ce collaborateur n'est pas un membre du support.")

        event.support_contact_id = support.id
        session.commit()
        session.refresh(event)
        return event

@sentry_wrap
def create_event_for_client(current_user, contract_id, start_date, end_date, location, attendiees, notes, support_id=None):
    with SessionLocal() as session:
        data= [contract_id, start_date, end_date, location, attendiees]
        if end_date < start_date:
            raise ValueError("Erreur, la date de debut est supérieur à la date de fin.")
        if not all(data):
            raise ValueError("Les champs suivant sont obligatoires : contract_id, start_date, end_date, location, attendiees, notes ")
        contract = session.query(Contract).filter_by(id=contract_id).first()
        if not contract:
            raise ValueError("Aucun contrat trouvé.")
        if contract.commercial_id != current_user.id:
            raise ValueError("Ce contrat ne vous apparient pas.")
        if not contract.statut:
            raise ValueError("Le contrat n'est pas encore signé.")
        
        new_event = Event(
            start_date=start_date,
            end_date=end_date,
            location=location,
            attendiees=attendiees, 
            notes=notes,
            contract_id=contract_id,
            client_id=contract.client_id,
            support_contact_id=support_id
        )

        session.add(new_event)
        session.commit()
        session.refresh(new_event)

        return new_event


@sentry_wrap  
def update_event(event_id, **updates):
    with SessionLocal() as session:
        event = session.query(Event).filter_by(id=event_id).first()

        for key, value in updates.items():
            if value is not None and hasattr(event, key):
                setattr(event, key, value)

        session.commit()
        session.refresh(event)

        return event