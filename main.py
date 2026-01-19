import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

API_KEY = os.getenv("API_KEY")

app = FastAPI(title="Trading Metrics API")

# ---------- MODELOS ----------

class Trade(BaseModel):
    run_id: str
    instrument: str
    pnl: float
    r: float
    mfe: float
    mae: float
    entry_time: str
    exit_time: str

# ---------- AUTH ----------

def auth(authorization: str | None = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

# ---------- ENDPOINTS ----------

@app.get("/")
def root():
    return {"status": "trading-api running"}

@app.get("/health")
def health():
    return {"status": "alive"}

@app.post("/trade")
def ingest_trade(trade: Trade, authorization: str | None = Header(None)):
    auth(authorization)

    # aquí luego va DB insert
    return {
        "status": "ok",
        "instrument": trade.instrument,
        "pnl": trade.pnl
    }
