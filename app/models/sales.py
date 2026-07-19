from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Sale(Base):
    """A single sale (stock-out) transaction for one product to one customer."""
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)

    customer_name = Column(String(150), nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)  # quantity * unit_price, stored for audit stability

    reference_no = Column(String(80), nullable=True)  # invoice/receipt number
    notes = Column(String(500), nullable=True)

    sale_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    product = relationship("Product", back_populates="sales")
    created_by_user = relationship("User", back_populates="sales")
