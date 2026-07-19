from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Purchase(Base):
    """A single purchase (stock-in) transaction for one product from one supplier."""
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)

    supplier_name = Column(String(150), nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_cost = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)  # quantity * unit_cost, stored for audit stability

    reference_no = Column(String(80), nullable=True)  # invoice/PO number
    notes = Column(String(500), nullable=True)

    purchase_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    product = relationship("Product", back_populates="purchases")
    created_by_user = relationship("User", back_populates="purchases")
