from datetime import date, datetime
from typing import Optional

from fastapi import HTTPException, status


def ensure_positive_stock(current_stock: int, requested_quantity: int) -> None:
    """Raise 400 if a sale/removal would drive stock below zero."""
    if requested_quantity > current_stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Insufficient stock: requested {requested_quantity}, "
                f"only {current_stock} available."
            ),
        )


def parse_date_range(start_date: Optional[date], end_date: Optional[date]) -> None:
    """Raise 400 if start_date is after end_date."""
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date cannot be after end_date.",
        )


def end_of_day(d: date) -> datetime:
    """Convert a date to the last microsecond of that day, for inclusive range filtering."""
    return datetime.combine(d, datetime.max.time())


def start_of_day(d: date) -> datetime:
    return datetime.combine(d, datetime.min.time())
