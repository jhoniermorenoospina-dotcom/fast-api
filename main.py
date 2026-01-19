import os
from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy.orm import Session

from db import SessionLocal
from models import Trade as TradeModel
from schemas import TradeSchema

API_KEY = os.getenv("API_KEY")

app = FastAPI(title="Trading Metrics API")

# ---------- AUTH ----------
def auth(authorization: str = Header(..., alias="Authorization")):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

# ---------- DB DEP ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    authorization: str = Header(..., alias="Authorization"),
    db: Session = Depends(get_db)
):
    auth(authorization)

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
