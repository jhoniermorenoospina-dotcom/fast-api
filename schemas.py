from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

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
