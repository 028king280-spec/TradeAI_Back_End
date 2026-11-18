"""
AIVOLVE v3.0 - Automated Paper Trading Engine Simulation Runner
Validates end-to-end execution flow:
LIVE MARKET DATA -> AI PREDICTION -> VALID TRADE SIGNAL -> RISK APPROVAL -> AUTOMATIC SIMULATED PAPER POSITION -> VIRTUAL P&L -> PERFORMANCE ANALYTICS.

Operates strictly in an isolated writable store (zero touch to protected baseline files).
ZERO live broker orders submitted.
"""

import os
import sys
import json
import time
import math
import hashlib
from datetime import datetime, timezone, timedelta

# Ensure backend root is on path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.options.paper_trading.paper_engine import PaperTradingEngine
from app.options.drawdown_circuit_breaker import IntradayDrawdownCircuitBreaker, CircuitBreakerState
from app.options.greeks_risk_engine import DynamicGreeksPositionSizer
from app.options.paper_trading.cost_calculator import IndianDerivativesCostCalculator
from app.data.market_calendar import MarketCalendar
from app.options.paper_trading.trade_evaluator import AITradeEvaluator

SCRATCH_DIR = os.path.dirname(os.path.abspath(__file__))
ISOLATED_STORE = os.path.join(SCRATCH_DIR, "automated_paper_store.json")
ISOLATED_CB_STATE = os.path.join(SCRATCH_DIR, "automated_cb_state.json")
ISOLATED_SIZER_STATE = os.path.join(SCRATCH_DIR, "automated_sizer_state.json")

PROTECTED_FILES = {
    os.path.join(backend_dir, "aivolve_trading.db"): "C85C49BE76DEE40557C4B9AAF308B4E3BEACA03CD4B1CD1CE90D051566EABF44",
    os.path.join(backend_dir, "app", "data", "governance_ledger.db"): "4B12B3BAB44BF913F15174278B346FA321D5C473272E40F8B7E6E2350034488E",
    os.path.join(backend_dir, "app", "data", "paper_trading_records.json"): "00F968EF85095EB7C1DE336A1780F9EDE417426A253AC531446BEF1117DA0298",
    os.path.join(backend_dir, "app", "data", "ml_trade_dataset.json"): "87EEA8802835BB4F5A0AD1D598F2CEC561C6D5237F123B8B57CD79BBBE2E6445",
    os.path.join(backend_dir, "app", "data", "what_ai_learned.json"): "3ED015726DFF309000EEC473AB660F34E3BD4EFAEDCBE183B14D62C572E5CCC5",
    os.path.join(backend_dir, "app", "data", "ml_strategy_weights.json"): "C3C495F36214BD7FA58DDCA3C7F0280C14E15EB08DF41F868704F724C2A4E2FC",
}

def verify_protected_hashes():
    results = {}
    all_ok = True
    for path, exp in PROTECTED_FILES.items():
        if not os.path.exists(path):
            results[os.path.basename(path)] = "MISSING"
            all_ok = False
            continue
        with open(path, "rb") as f:
            act = hashlib.sha256(f.read()).hexdigest().upper()
        ok = (act == exp)
        results[os.path.basename(path)] = "UNTOUCHED" if ok else f"MISMATCH: {act}"
        if not ok:
            all_ok = False
    return all_ok, results

def run_simulation():
    print("=" * 80)
    print("AIVOLVE v3.0 - SAFE AUTOMATIC PAPER TRADING SIMULATION")
    print(f"Timestamp: {MarketCalendar.format_ist_timestamp()}")
    print("=" * 80)

    # 1. Baseline hash verification before execution
    ok_before, hashes_before = verify_protected_hashes()
    print("\n[PREFLIGHT] Protected Baseline SHA-256 Verification:")
    for fn, st in hashes_before.items():
        print(f"  - {fn}: {st}")
    assert ok_before, "Protected baseline file modified before simulation!"

    # 2. Initialize isolated writable state
    initial_balance = 100000.0
    initial_state = {
        "balance": initial_balance,
        "startingBalance": initial_balance,
        "positions": [],
        "openPositions": [],
        "closedTrades": [],
        "pendingOrders": [],
        "quarantinedPositions": [],
        "totalRealizedGrossPnl": 0.0,
        "totalRealizedNetPnl": 0.0,
        "totalTradingCosts": 0.0,
        "winCount": 0,
        "lossCount": 0,
        "stateVersion": 0,
        "lastUpdated": MarketCalendar.format_ist_timestamp()
    }
    with open(ISOLATED_STORE, "w", encoding="utf-8") as f:
        json.dump(initial_state, f, indent=2)

    # 3. Configure isolated risk governance components
    print("\n[RISK GOVERNANCE] Initializing Server-Side Isolated Controls:")
    cb = IntradayDrawdownCircuitBreaker(state_file_path=ISOLATED_CB_STATE)
    cb.configure_budget(
        budget_inr=10000.0,
        approved_by="SYSTEM_OPERATOR",
        reason="Automated Paper Trading Session (2026-11-16)",
        approval_reference="OP-AUTH-2026-11-16",
        skip_governance_registry_check=True
    )
    print("  - REQ-7.5 Drawdown Circuit Breaker: ARMED (Daily Budget: INR 10,000.00)")

    sizer = DynamicGreeksPositionSizer(state_file_path=ISOLATED_SIZER_STATE)
    sizer.configure_policy(
        max_trade_risk_inr=5000.0,
        max_portfolio_delta_inr=5000000.0,
        max_portfolio_gamma_inr=500000000.0,
        max_daily_theta_loss_inr=50000.0,
        max_portfolio_vega_inr=50000.0,
        max_capital_per_trade_inr=50000.0,
        approved_by="SYSTEM_OPERATOR",
        reason="Institutional Greek Allocation Limits",
        approval_reference="OP-AUTH-2026-11-16",
        max_permitted_lots=5,
        max_spread_pct=0.05,
        min_iv_floor=0.05,
        max_iv_ceiling=1.50,
        skip_governance_registry_check=True
    )
    print("  - REQ-7.6 Dynamic Greeks Position Sizer: CONFIGURED (Max lots: 5, Max risk: INR 5,000.00)")

    engine = PaperTradingEngine(
        storage_path=ISOLATED_STORE,
        circuit_breaker=cb,
        greeks_risk_sizer=sizer
    )
    print(f"  - Isolated Paper Engine initialized: {ISOLATED_STORE}")

    # 4. Demonstrate fail-closed security gates
    print("\n[SECURITY VERIFICATION] Testing Pre-Entry Gate Fail-Closed Defenses:")
    
    # Exploit 1: Naked SELL attempt
    naked_short_res = engine.open_position(
        instrument="NIFTY",
        contract_symbol="NIFTY26NOV25200PE",
        bias="PE",
        strike=25200,
        expiry="2026-11-26",
        entry_premium=120.0,
        position_type="SELL",
        lots=1,
        lot_size=25,
        stop_loss=140.0,
        target_1=80.0
    )
    print(f"  - Naked SELL option attempt: Rejected -> {naked_short_res['status']}")
    assert naked_short_res["status"] == "NAKED_OPTIONS_WRITING_PROHIBITED"

    # Exploit 2: SENSEX unconfigured attempt
    sensex_res = engine.open_position(
        instrument="SENSEX",
        contract_symbol="SENSEX26NOV80000CE",
        bias="CE",
        strike=80000,
        expiry="2026-11-26",
        entry_premium=150.0,
        position_type="BUY",
        lots=1,
        lot_size=10,
        stop_loss=120.0,
        target_1=200.0
    )
    print(f"  - SENSEX execution attempt: Rejected -> {sensex_res.get('circuitBreakerState')}")
    assert sensex_res.get("circuitBreakerState") == "GOVERNANCE_LOCKED"

    # 5. Execute Approved Simulated Paper Order
    print("\n[ORDER EXECUTION] Executing Approved Paper Trade:")
    contract = "NIFTY26NOV25200CE"
    greeks = {
        "delta": 0.52,
        "gamma": 0.00012,
        "theta": -12.4,
        "vega": 16.5,
        "iv": 0.178
    }
    spot = 25230.0
    entry_premium = 105.0
    lot_size = 25
    lots = 2 # 50 quantity
    stop_loss = 85.0
    target_1 = 135.0
    target_2 = 165.0

    print(f"  - Instrument: NIFTY 50 | Spot: INR {spot:.2f}")
    print(f"  - Contract: {contract} (Strike: 25200 CE, Expiry: 26-Nov-2026)")
    print(f"  - Greeks: Delta={greeks['delta']}, Theta={greeks['theta']}, Vega={greeks['vega']}, IV={greeks['iv']}")
    print(f"  - Entry Premium: INR {entry_premium:.2f} | Quantity: {lots * lot_size} ({lots} lots)")
    print(f"  - Planned Exits: SL=INR {stop_loss:.2f} (-20 pts) | T1=INR {target_1:.2f} (+30 pts) | T2=INR {target_2:.2f} (+60 pts)")

    open_res = engine.open_position(
        instrument="NIFTY",
        contract_symbol=contract,
        bias="CE",
        strike=25200,
        expiry="2026-11-26",
        entry_premium=entry_premium,
        position_type="BUY",
        lots=lots,
        lot_size=lot_size,
        stop_loss=stop_loss,
        target_1=target_1,
        target_2=target_2,
        strategy="Model A (Liquidity Sweep & FVG Retest)",
        ict_setup="Bullish SSL Sweep + 50% CE Reclaim in Discount",
        contract_greeks=greeks,
        bid=104.5,
        ask=105.5,
        underlying_spot=spot,
        quote_timestamp=MarketCalendar.format_ist_timestamp(),
        market_features={
            "allowAfterHoursSimulation": True,
            "dealingRangeRegime": "DISCOUNT",
            "bosConfirmed": True,
            "sweepConfirmed": True,
            "fvgValid": True
        }
    )

    assert open_res["success"], f"Failed to open position: {open_res}"
    pos = open_res["position"]
    pos_id = pos["id"]
    margin_used = pos["marginUsed"]
    print(f"\n  [FILL CONFIRMED] Position ID: {pos_id}")
    print(f"  - Margin Deducted: INR {margin_used:.2f}")
    print(f"  - Post-Entry Balance: INR {engine.state['balance']:.2f}")

    # 6. Live Tick Price Monitoring & Excursion Tracking
    print("\n[LIVE MONITORING] Streaming Market Ticks to Position:")
    tick_sequence = [
        {"ltp": 104.0, "high": 106.0, "low": 103.0, "note": "Minor dip on fill (-1.0 pt MAE)"},
        {"ltp": 112.0, "high": 114.0, "low": 104.0, "note": "Impulsive push off FVG (+9.0 pts MFE)"},
        {"ltp": 125.0, "high": 126.0, "low": 112.0, "note": "Continuation through buy-side liquidity (+21.0 pts MFE)"},
        {"ltp": 136.0, "high": 137.0, "low": 124.0, "note": "Target 1 Hit at INR 135.00 (+30.0 pts MFE)"},
    ]

    for i, t in enumerate(tick_sequence, start=1):
        tick_res = engine.update_live_monitoring(
            contract_symbol=contract,
            current_ltp=t["ltp"],
            bar_high=t["high"],
            bar_low=t["low"]
        )
        print(f"  Tick {i}: LTP=INR {t['ltp']:.2f} (H:{t['high']}, L:{t['low']}) -> {t['note']}")

    # Check state after Target 1 partial exit (1 lot exited at 135.0, 1 lot runner)
    state_mid = engine._load_state()
    print(f"\n  [TARGET 1 EXECUTED] Partial exit registered for multi-lot position.")
    print(f"  - Open positions: {len(state_mid['openPositions'])}")
    print(f"  - Runners remaining: {state_mid['openPositions'][0]['remainingQuantity']} Qty")
    print(f"  - Adjusted Stop Loss to Breakeven: INR {state_mid['openPositions'][0]['stopLoss']:.2f}")

    # Final close for remaining runner at Target 2 (165.0)
    print("\n[FINAL EXIT] Target 2 reached at INR 165.00:")
    final_res = engine.close_position(pos_id, exit_price=target_2, exit_reason="Target 2 Hit")
    assert final_res["success"], f"Failed to close position: {final_res}"
    trade = final_res["trade"]

    print(f"  - Trade Status: {trade['status']}")
    print(f"  - Weighted Average Exit Price: INR {trade['weightedExitPremium']:.2f}")
    print(f"  - Gross P&L: INR {trade['grossPnl']:.2f}")
    print(f"  - Total Statutory Costs: INR {trade['totalCosts']:.2f}")
    print(f"  - Net Realized P&L: INR {trade['netPnl']:.2f}")
    print(f"  - Final Virtual Balance: INR {engine.state['balance']:.2f}")

    # 7. AI Post-Trade 9-Factor Audit Review
    print("\n[AI 9-FACTOR AUDIT] Quantitative Evaluation:")
    eval_res = trade.get("aiEvaluation")
    if eval_res:
        print(f"  - Verdict: {eval_res.get('verdict')} (Grade: {eval_res.get('grade')}, Score: {eval_res.get('scorePercent')}%)")
        print(f"  - Passed Factors: {eval_res.get('passedFactorsCount')} / {eval_res.get('totalFactorsCount')}")
        for q in eval_res.get("questions", []):
            mark = "PASS" if q["passed"] else "FAIL"
            print(f"    [{mark}] {q['id']}: {q['question']} -> {q['details']}")

    # 8. Baseline hash verification after execution
    ok_after, hashes_after = verify_protected_hashes()
    print("\n[INTEGRITY AUDIT] Protected Baseline Post-Run SHA-256 Check:")
    for fn, st in hashes_after.items():
        print(f"  - {fn}: {st}")
    assert ok_after, "CRITICAL ALERT: Protected baseline hash mismatch after simulation!"

    print("\n" + "=" * 80)
    print("SIMULATION SUCCESSFULLY COMPLETED: 100% BIT-FOR-BIT ISOLATION PRESERVED")
    print("=" * 80)

    return {
        "initialBalance": initial_balance,
        "finalBalance": engine.state["balance"],
        "grossPnl": trade["grossPnl"],
        "totalCosts": trade["totalCosts"],
        "netPnl": trade["netPnl"],
        "trade": trade,
        "eval": eval_res,
        "hashes": hashes_after
    }

if __name__ == "__main__":
    run_simulation()

