from sqlalchemy import Column, Integer, String, func, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, index=True)
    total_amount = Column(Integer, nullable=False)
    amount_left = Column(Integer, nullable=False)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    statut = Column(Boolean, nullable=False, default=False)

    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    client = relationship("Client", back_populates="contracts")

    commercial_id = Column(Integer, ForeignKey('collaborateurs.id'), nullable=False)
    commercial = relationship("Collaborateur", back_populates="contracts")

    events = relationship("Event", back_populates="contract")
