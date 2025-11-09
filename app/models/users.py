from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.security.hash import PasswordManager
from app.models.contracts import Contract
from app.models.events import Event

class Collaborateur(Base):
    __tablename__ = 'collaborateurs'
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    departement = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    role = relationship("Role", back_populates="collaborateurs")
    password_hash = Column(String, nullable=False)
    contracts = relationship('Contract', back_populates='commercial')
    events_support = relationship('Event', back_populates='support_contact')

    def set_password(self, password: str):
        self.password_hash = PasswordManager.hash_password(password)

    def check_password(self, password: str) -> bool:
        return PasswordManager.verify_password(self.password_hash, password)

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, nullable=False)
    collaborateurs = relationship("Collaborateur", back_populates="role")