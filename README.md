# Epic Events — CRM Interne (CLI)

CRM interne développé pour l'entreprise **Epic Events**, organisatrice d'événements.

L'objectif de ce projet est de fournir un outil en ligne de commande permettant de gérer :  
- Clients  
- Contrats  
- Événements  
- Collaborateurs & permissions  

Le projet respecte les bonnes pratiques de sécurité (principe du moindre privilège, prévention injections SQL) et intègre **Sentry** pour la journalisation des erreurs.

---

## Objectifs

- Centraliser les informations clients / contrats / événements  
- Sécuriser l’accès selon les rôles  
- Fournir une interface CLI simple et fiable  
- Journaliser les erreurs via Sentry

---

## Technologies

| Domaine | Outil |

Langage : Python 3.10+ |
ORM : SQLAlchemy |
CLI : Click |
DB : PostgreSQL 
Logs : Sentry |
Tests : Pytest + Coverage |
Sécurité : RBAC, hashing mot de passe |

---

## 📂 Structure du projet

``` bash
.
├── app/
│ ├── cli/
│ ├── controllers/
│ ├── crud/
│ ├── db/
│ ├── models/
│ ├── security/
│ ├── sentry/
│ ├── main.py
| ├── utils.py
| └── tests/
| 
├── requirements.txt
├── README.md
└── diagramme.md

```

## Fonctionnalités par rôle

### Collaborateurs & accès

| Rôle | Capabilités |
|------|-------------|
| Gestion | CRUD collaborateurs, contrats, assignation support |
| Commercial | CRUD clients + événements pour leurs clients |
| Support | Gestion uniquement des événements qui leur sont attribués |

---

## Données

### Client
- Nom complet  
- Email  
- Téléphone  
- Société  
- Date création / dernier contact  
- Commercial associé  

### Contrat
- Client  
- Commercial  
- Montant total & restant  
- Statut (signé / non signé)  
- Date création  

### Événement
- Client & contrat associés  
- Support assigné  
- Dates  
- Lieu  
- Nb invités  
- Notes  

> Schéma de base de données disponible dans `diagramme.md`

---

## Sécurité

- Hash des mots de passe  
- RBAC — principe du moindre privilège  
- Sessions utilisateur  
- ORM = protection contre injection SQL  

---

## Journalisation (Sentry)

Log automatique :
- Erreurs
- Exceptions

---

## Installation & exécution

```bash
git clone <repo>
cd epic_events_crm

python3 -m venv env
source env/bin/activate

pip install -r requirements.txt

# Commandes exemples
python -m app.main.py login
python app.main.py gestion-menu
python app.main.py commercial-menu
python app.main.py support-menu

# Tests & couverture
pytest -v

# Authentification
Système basé sur email + mot de passe
Session générée après login, supprimée à la déconnexion
