from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    location = Column(String, nullable=False)  
    attendiees = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)

    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    contract = relationship("Contract", back_populates="events")

    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    client = relationship("Client", back_populates="events")

    support_contact_id = Column(Integer, ForeignKey('collaborateurs.id'), nullable=True)
    support_contact = relationship("Collaborateur", back_populates="events_support")

