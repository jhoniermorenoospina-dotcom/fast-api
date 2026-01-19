from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# ---------- TRADE ----------
class TradeSchema(BaseModel):
    run_id: UUID
    instrument: str
    entry_time: datetime
    exit_time: datetime
    pnl: float
    r: float
    mfe: float
    mae: float
    direction: str

# ---------- STRATEGY RUN ----------
class StrategyRunCreate(BaseModel):
    instrument: str
    start_time: Optional[datetime] = None
    rr: Optional[float] = None
    be_rr: Optional[float] = None
    trailing_rr: Optional[float] = None
    stop_type: Optional[str] = None
