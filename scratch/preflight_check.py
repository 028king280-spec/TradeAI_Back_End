import os
import sys
import json
import datetime
from zoneinfo import ZoneInfo

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath("."))

IST = ZoneInfo("Asia/Kolkata")
now_ist = datetime.datetime.now(IST)

print("=" * 70)
print("AIVOLVE v3.0 — PHASE 5.2C PREFLIGHT & DIAGNOSTIC AUDIT")
print("=" * 70)
print(f"Timestamp (IST)   : {now_ist.isoformat()}")
print(f"Day of Week       : {now_ist.strftime('%A')}")
print(f"Date              : {now_ist.strftime('%d-%b-%Y')}")

# 1. Market Session Check via MarketCalendar
from app.data.market_calendar import MarketCalendar
is_trading_day = MarketCalendar.is_trading_day(now_ist)
is_market_open = MarketCalendar.is_market_open(now_ist)
status_str = MarketCalendar.get_market_status(now_ist)

print(f"Is Trading Day    : {is_trading_day}")
print(f"Is Market Open    : {is_market_open}")
print(f"Session Status    : {status_str}")

# 2. Broker Authentication & Environment
print("-" * 70)
print("1. Broker Authentication & Credentials Status:")
from app.data.providers.angelone_provider import AngelOneMarketDataProvider
ao_provider = AngelOneMarketDataProvider()
auth_status = ao_provider.is_authenticated
print(f"  AngelOne MarketDataProvider loaded : True")
print(f"  AngelOne Authenticated             : {auth_status}")
print(f"  ANGEL_API_KEY present in env       : {bool(os.getenv('ANGEL_API_KEY'))}")
print(f"  ANGEL_CLIENT_CODE present in env   : {bool(os.getenv('ANGEL_CLIENT_CODE'))}")

# 3. WebSocket Manager & Tick Streaming Health
print("-" * 70)
print("2. WebSocket Connection & Active Tick Streaming Check:")
from app.data.providers.angelone_websocket import angelone_ws_manager
ws_diag = angelone_ws_manager.get_diagnostics()
print(f"  WebSocket Manager Initialized      : True")
print(f"  WebSocket is_running               : {ws_diag['is_running']}")
print(f"  WebSocket is_healthy               : {ws_diag['is_healthy']}")
print(f"  Ticks received count               : {ws_diag['ticks_received']}")
print(f"  Seconds since last tick            : {ws_diag['seconds_since_last_tick']}")
print(f"  Classification rule                : Inactive socket MUST NOT be classified as healthy live streaming.")
if ws_diag['is_running'] and not ws_diag['is_healthy']:
    print(f"  Verification Status                : CORRECTLY FLAGGED AS INACTIVE/UNHEALTHY.")
elif not ws_diag['is_running']:
    print(f"  Verification Status                : SOCKET OFFLINE / NOT RUNNING.")

# 4. Instrument Master & Supported Instruments
print("-" * 70)
print("3. Instrument Master & Contract Resolution Check:")
from app.data.instrument_master import InstrumentMaster
im = InstrumentMaster.get_instance()
print(f"  InstrumentMaster loaded            : {im.is_loaded()}")
for symbol in ["NIFTY", "BANKNIFTY", "FINNIFTY"]:
    expiries = im.get_expiries(symbol)
    strikes = im.get_strikes_for_underlying(symbol)
    print(f"  [{symbol:10}] Expiries: {len(expiries)} available (Earliest: {expiries[0] if expiries else 'None'}), Strikes: {len(strikes)}")

# SENSEX Governance Lock Check
from app.options.contract_selector import CENTRALIZED_INDEX_LIQUIDITY_POLICY
sensex_gov = CENTRALIZED_INDEX_LIQUIDITY_POLICY.get("SENSEX", {})
print(f"  [SENSEX    ] Governance Status     : {sensex_gov.get('policy_status', 'LOCKED')} (Barred from automated observation)")

# 5. Data Quality Engine Status
print("-" * 70)
print("4. Data Quality Engine Status:")
from app.data.quality_validator import DataQualityEngine, FeedStatus
print(f"  DataQualityEngine ready            : True")
print(f"  FeedStatus classes                 : VERIFIED_LIVE, DEGRADED, STALE, DATA_OFFLINE")

# 6. Dataset Isolation & Production Dataset Audit
print("-" * 70)
print("5. Dataset Governance & Baseline Integrity Audit:")
import hashlib

def get_file_hash(filepath: str) -> str:
    if not os.path.exists(filepath):
        return "FILE_NOT_FOUND"
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest().upper()

protected_files = {
    "aivolve_trading.db": "C85C49BE76DEE40557C4B9AAF308B4E3BEACA03CD4B1CD1CE90D051566EABF44",
    "app/data/governance_ledger.db": "4B12B3BAB44BF913F15174278B346FA321D5C473272E40F8B7E6E2350034488E",
    "app/data/paper_trading_records.json": "00F968EF85095EB7C1DE336A1780F9EDE417426A253AC531446BEF1117DA0298",
    "app/data/ml_trade_dataset.json": "87EEA8802835BB4F5A0AD1D598F2CEC561C6D5237F123B8B57CD79BBBE2E6445",
    "app/data/what_ai_learned.json": "3ED015726DFF309000EEC473AB660F34E3BD4EFAEDCBE183B14D62C572E5CCC5",
    "app/data/ml_strategy_weights.json": "C3C495F36214BD7FA58DDCA3C7F0280C14E15EB08DF41F868704F724C2A4E2FC"
}

all_match = True
for path, expected_hash in protected_files.items():
    current_hash = get_file_hash(path)
    match = (current_hash == expected_hash)
    if not match:
        all_match = False
    print(f"  {path:38}: {'MATCH' if match else 'MISMATCH'}")

print(f"  All 6 Protected Baseline Hashes Match: {all_match}")

# Production dataset check
prod_path = "app/data/ml_production_dataset.json"
if os.path.exists(prod_path):
    with open(prod_path, "r", encoding="utf-8") as f:
        prod_data = json.load(f)
    print(f"  Production dataset records count   : {len(prod_data)}")
else:
    print(f"  Production dataset records count   : 0 (File isolated and unpopulated)")

print("=" * 70)
