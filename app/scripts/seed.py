from datetime import date
from app.db.base import SessionLocal, engine, Base
from app.models.users import Collaborateur, Role
from app.models.clients import Client
from app.models.contracts import Contract
from app.models.events import Event

# --- Initialisation de la base ---
Base.metadata.create_all(bind=engine)
session = SessionLocal()

try:
    # --- Rôles ---
    role_gestion = Role(nom="gestion")
    role_commercial = Role(nom="commercial")
    role_support = Role(nom="support")

    session.add_all([role_gestion, role_commercial, role_support])
    session.commit()

    # --- Collaborateurs ---
    gestionnaire = Collaborateur(
        prenom="Gabriel",
        nom="Martin",
        email="gabriel.martin@epic.com",
        departement="Gestion",
        role=role_gestion,  
    )
    gestionnaire.set_password("admin123")

    commercial = Collaborateur(
        prenom="Camille",
        nom="Durand",
        email="camille.durand@epic.com",
        departement="Commercial",
        role=role_commercial,
    )
    commercial.set_password("sales123")

    support = Collaborateur(
        prenom="Sarah",
        nom="Morel",
        email="sarah.morel@epic.com",
        departement="Support",
        role=role_support,
    )
    support.set_password("support123")

    session.add_all([gestionnaire, commercial, support])
    session.commit()

    # --- Clients ---
    client1 = Client(
        fullname="John Quick",
        email="john.quick@gmail.com",
        telephone="+1 234 567 8901",
        entreprise="Quick Events Inc.",
        date_created=str(date(2021, 4, 18)),
        date_updated=str(date(2023, 3, 29)),
        commercial_id=commercial.id
    )

    client2 = Client(
        fullname="Kevin Casey",
        email="kevin@startup.io",
        telephone="+678 123 456 78",
        entreprise="Cool Startup LLC",
        date_created=str(date(2021, 4, 18)),
        date_updated=str(date(2023, 3, 29)),
        commercial_id=commercial.id
    )

    session.add_all([client1, client2])
    session.commit()

    # --- Contrats ---
    contract1 = Contract(
        client_id=client1.id,
        commercial_id=commercial.id,
        total_amount=5000,
        amount_left=1000,
        date_created=date(2023, 1, 10),
        statut=True
    )

    contract2 = Contract(
        client_id=client2.id,
        commercial_id=commercial.id,
        total_amount=7500,
        amount_left=7500,
        date_created=date(2023, 3, 5),
        statut=False
    )

    session.add_all([contract1, contract2])
    session.commit()

    # --- Événements ---
    event1 = Event(
        contract_id=contract1.id,
        client_id=client1.id,
        start_date=date(2023, 6, 4),
        end_date=date(2023, 6, 5),
        support_contact_id=support.id,
        location="53 Rue du Château, 41120 Candé-sur-Beuvron, France",
        attendiees=75,
        notes="Wedding starts at 3PM, by the river. Catering is organized."
    )

    event2 = Event(
        contract_id=contract2.id,
        client_id=client2.id,
        start_date=date(2024, 9, 10),
        end_date=date(2024, 9, 12),
        support_contact_id=support.id,
        location="Tech Hub, 15 rue Montgallet, Paris",
        attendiees=120,
        notes="Startup event for Cool Startup LLC."
    )

    session.add_all([event1, event2])
    session.commit()

    print("✅ Données de test insérées avec succès !")

except Exception as e:
    print("❌ Erreur pendant le seed :", e)
    session.rollback()

finally:
    session.close()
