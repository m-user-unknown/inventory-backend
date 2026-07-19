from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(150), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    category = Column(String(100), nullable=True, index=True)
    unit = Column(String(20), default="pcs", nullable=False)  # e.g. pcs, kg, box

    unit_price = Column(Float, nullable=False, default=0.0)  # current selling price
    cost_price = Column(Float, nullable=False, default=0.0)  # last known purchase cost

    quantity_in_stock = Column(Integer, nullable=False, default=0)
    reorder_level = Column(Integer, nullable=False, default=10)

    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    purchases = relationship("Purchase", back_populates="product")
    sales = relationship("Sale", back_populates="product")
