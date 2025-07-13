from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from .database import get_db
from . import crud

app = FastAPI()

@app.get("/stocks")
def get_all_stocks(page: int = 1, count: int = 25, db: Session = Depends(get_db)):
    return crud.get_paginated_stocks(db, page, count)

@app.get("/stocks/{symbol}")
def get_stock_details(
    symbol: str,
    price: float = None,
    quantity: int = None,
    date: str = None,
    page: int = 1,
    count: int = 25,
    db: Session = Depends(get_db)
):
    return crud.filter_stocks(symbol, price, quantity, date, page, count, db)
