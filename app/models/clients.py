from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telephone = Column(String, nullable=False)
    entreprise = Column(String, nullable=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    commercial_id = Column(Integer, ForeignKey('collaborateurs.id'), nullable=False)
    commercial = relationship("Collaborateur")

    contracts = relationship("Contract", back_populates="client")
    events = relationship("Event", back_populates="client")

