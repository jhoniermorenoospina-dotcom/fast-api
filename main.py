import os
from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session

from db import SessionLocal
from models import Trade as TradeModel
from schemas import TradeSchema

API_KEY = os.getenv("API_KEY")

app = FastAPI(title="Trading Metrics API")

# ---------- DB ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- AUTH ----------
def auth(request: Request):
    auth_header = request.headers.get("authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    if auth_header != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

# ---------- ENDPOINTS ----------

@app.get("/")
def root():
    return {"status": "trading-api running"}

@app.get("/health")
def health():
    return {"status": "alive"}

@app.post("/trade")
def ingest_trade(
    trade: TradeSchema,
    request: Request,
    db: Session = Depends(get_db)
):
    auth(request)

    db_trade = TradeModel(
        run_id=trade.run_id,
        instrument=trade.instrument,
        entry_time=trade.entry_time,
        exit_time=trade.exit_time,
        pnl=trade.pnl,
        r=trade.r,
        mfe=trade.mfe,
        mae=trade.mae,
        direction=trade.direction
    )

    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)

    return {
        "status": "saved",
        "trade_id": db_trade.id
    }
