from sqlalchemy.orm import Session
from .models import Stock

def get_paginated_stocks(db: Session, page: int, count: int):
    offset = (page - 1) * count
    return (
        db.query(Stock)
        .order_by(Stock.timestamp.desc())
        .offset(offset)
        .limit(count)
        .all()
    )

def filter_stocks(symbol: str, price: float, quantity: int, date: str, page: int, count: int, db: Session):
    query = db.query(Stock).filter(Stock.symbol == symbol)

    if price is not None:
        query = query.filter(Stock.price <= price)
    if quantity is not None:
        query = query.filter(Stock.quantity <= quantity)
    if date is not None:
        query = query.filter(Stock.timestamp.like(f"{date}%"))

    offset = (page - 1) * count
    return query.order_by(Stock.timestamp.desc()).offset(offset).limit(count).all()
