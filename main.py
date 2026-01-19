import os
import uuid
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

from db import SessionLocal
from models import Trade as TradeModel
from models import StrategyRun as StrategyRunModel
from schemas import TradeSchema, StrategyRunCreate

API_KEY = os.getenv("API_KEY")

app = FastAPI(title="Trading Metrics API")

# ---------- CORS (CRÍTICO) ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://readme-parser--shoniermoreno.replit.app",
        "https://trade-parser--shoniermoreno.replit.app",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# ---------- CREATE STRATEGY RUN ----------
@app.post("/strategy-run")
def create_strategy_run(
    payload: StrategyRunCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    auth(request)

    run_id = uuid.uuid4()

    db_run = StrategyRunModel(
        id=run_id,
        instrument=payload.instrument,
        start_time=payload.start_time or datetime.utcnow(),
        rr=payload.rr,
        be_rr=payload.be_rr,
        trailing_rr=payload.trailing_rr,
        stop_type=payload.stop_type
    )

    db.add(db_run)
    db.commit()
    db.refresh(db_run)

    return {
        "status": "created",
        "run_id": str(run_id)
    }

# ---------- INGEST TRADE ----------
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

# ---------- DASHBOARD RANKING ----------
@app.get("/dashboard/ranking")
