from sqlalchemy.orm import joinedload
from app.sentry.decorateur_sentry import sentry_wrap
from app.db.base import SessionLocal
from app.models.contracts import Contract
from app.models.users import Collaborateur
from app.crud.collaborateurs_manager import get_commercial_by_fullname
from app.crud.events_manager import get_event_by_id
from app.crud.clients_manager import get_client_by_fullname

@sentry_wrap
def get_all_contracts(current_user):
    with SessionLocal() as session:
        contracts =  session.query(Contract).options(
            joinedload(Contract.client),
            joinedload(Contract.commercial),
            joinedload(Contract.events)
        ).all()
        
        return contracts

@sentry_wrap    
def get_contract_by_commercial(current_user, commercial_id):
    with SessionLocal() as session:
        contracts = session.query(Contract).options(
            joinedload(Contract.client),
            joinedload(Contract.commercial),
            joinedload(Contract.events)).filter_by(commercial_id=commercial_id).all()
        if not contracts:
            raise ValueError("Aucun contrat ne vous est attribué.")
        return contracts

@sentry_wrap
def get_contract_by_id(current_user, contract_id):
    with SessionLocal() as session:
        contract = session.query(Contract).filter_by(id=contract_id).first()
        if not contract:
            raise ValueError("Aucun contrat ne correspond à cet id.")

@sentry_wrap
def get_contract_not_signed(current_user):
    with SessionLocal() as session:
        query = session.query(Contract).options(
            joinedload(Contract.client),
            joinedload(Contract.commercial),
            joinedload(Contract.events)
        ).filter(Contract.statut == False)

        if current_user.role.nom == 'commercial':
            query = query.filter(Contract.commercial_id == current_user.id)

        contracts = query.all()
        if not contracts:
            raise ValueError("Aucun contrat non signé trouvé.")
        return contracts

@sentry_wrap
def get_contracts_not_fully_payed(current_user):
    with SessionLocal() as session:
        query = session.query(Contract).options(
            joinedload(Contract.client),
            joinedload(Contract.commercial),
            joinedload(Contract.events)
        ).filter(Contract.amount_left > 0)

        if current_user.role.nom == 'commercial':
            query = query.filter(Contract.commercial_id == current_user.id)

        contracts = query.all()
        if not contracts:
            raise ValueError("Tous les contrats sont entièrement payés.")
        return contracts
    

@sentry_wrap
def create_contract(current_user, total_amount, amount_left, client_fullname, commercial_fullname): 
    with SessionLocal() as session:
        data = [total_amount, amount_left, client_fullname, commercial_fullname]

        if not all(data):
            raise ValueError('Tous les champs sont obligatoires.')
        
        commercial = get_commercial_by_fullname(current_user, commercial_fullname)
        commercial_id = commercial.id
        client = get_client_by_fullname(current_user, client_fullname)
        client_id = client.id
    
        
        new_contract = Contract(
            total_amount=total_amount, 
            amount_left=amount_left,
            client_id=client_id,
            commercial_id = commercial_id
            )
    
        
        session.add(new_contract)
        session.commit()
        session.refresh(new_contract)

        return new_contract

@sentry_wrap
def updtate_contract(current_user, contract_id, **updates):
    with SessionLocal() as session:
        contract = session.query(Contract).filter_by(id=contract_id).first()

        if not contract:
            raise ValueError('Aucun contrat trouvé.')
        
        for key, value in updates.items():
            if value is not None and hasattr(contract, key):
                setattr(contract, key, value)

        session.commit()
        session.refresh(contract)
    
        return contract

@sentry_wrap
def update_clients_contracts(current_user, contract_id, **updates):
    with SessionLocal() as session:
        contract = session.query(Contract).filter_by(id=contract_id).first()
        if not contract:
            raise ValueError("Aucun contrat avec cet id n'a été trouvé.")
        
        if contract.commercial_id != current_user.id:
            raise ValueError("Ce contrat ne vous apparitent pas.")
        
        for key, value in updates.items():
            if hasattr(key, value):
                setattr(contract, key, value)

        session.commit()
        session.refresh(contract)
