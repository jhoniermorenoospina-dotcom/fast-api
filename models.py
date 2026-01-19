import uuid
from sqlalchemy import (
    Column, String, Integer, Float, Text,
    TIMESTAMP, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from db import Base

class StrategyRun(Base):
    __tablename__ = "strategy_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instrument = Column(Text, nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP)
    rr = Column(Float)
    be_rr = Column(Float)
    trailing_rr = Column(Float)
    stop_type = Column(Text)
    total_trades = Column(Integer, default=0)
    net_profit = Column(Float, default=0)
    max_drawdown = Column(Float, default=0)
    expectancy = Column(Float, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(UUID(as_uuid=True), ForeignKey("strategy_runs.id"))
    instrument = Column(Text)
    entry_time = Column(TIMESTAMP)
    exit_time = Column(TIMESTAMP)
    pnl = Column(Float)
    r = Column(Float)
    mfe = Column(Float)
    mae = Column(Float)
    direction = Column(Text)
