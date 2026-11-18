import sys, os, datetime
from zoneinfo import ZoneInfo
sys.path.insert(0, ".")
from app.options.paper_trading.observation_engine import ObservationEngine
from tests.test_observation_engine_phase5_2c import _get_valid_raw_features

engine = ObservationEngine()
open_dt = datetime.datetime(2026, 11, 16, 10, 0, 0, tzinfo=ZoneInfo("Asia/Kolkata"))
raw_feats = _get_valid_raw_features()
success, record, reason = engine.process_observation(
    underlying_symbol="NIFTY",
    contract_symbol="NIFTY26NOV25000CE",
    expiry_date="2026-11-26",
    strike_price=25000.0,
    option_type="CE",
    spot_ltp=25050.0,
    option_ltp=135.0,
    bid_price=134.5,
    ask_price=135.5,
    raw_market_data={},
    raw_features=raw_feats,
    observation_timestamp=open_dt,
)
print("success:", success)
print("reason:", reason)

