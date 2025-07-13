from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from fastapi import HTTPException
from .models import Stock

def get_paginated_stocks(db: Session, page: int, count: int):
    offset = (page - 1) * count

    # Subconsulta para obtener última actualización por símbolo
    subq = (
        db.query(
            Stock.symbol,
            func.max(Stock.timestamp).label("last_update")
        )
        .group_by(Stock.symbol)
        .subquery()
    )

    # Consultar la lista paginada de símbolos con última actualización
    query = db.query(
        subq.c.symbol,
        subq.c.last_update
    ).order_by(subq.c.symbol.asc()).offset(offset).limit(count)

    # Devolver como lista de diccionarios
    return [{"symbol": r.symbol, "last_update": r.last_update} for r in query.all()]

def filter_stocks(symbol: str, price: float, quantity: int, date: str, page: int, count: int, db: Session):
    query = db.query(Stock).filter(Stock.symbol == symbol)

    if price is not None:
        query = query.filter(Stock.price <= price)

    if quantity is not None:
        query = query.filter(Stock.quantity <= quantity)

    if date is not None:
        try:
            # Validar formato y comparar por fecha exacta
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            query = query.filter(func.date(Stock.timestamp) == date_obj)
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usa YYYY-MM-DD")

    offset = (page - 1) * count
    return query.order_by(Stock.timestamp.desc()).offset(offset).limit(count).all()
