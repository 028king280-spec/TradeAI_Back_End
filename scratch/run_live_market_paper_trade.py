"""
AIVOLVE v3.0 - LIVE MARKET PAPER TRADING ENGINE TEST
Connects to Angel One Live SmartAPI, captures genuine live market quotes,
executes a live paper trade at exact live LTP, and monitors tick progression.
Strictly PAPER_TRADING_ONLY. Never executes real broker orders.
"""

import asyncio
import datetime
import json
import os
import sys
import time

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.data.providers.angelone_provider import AngelOneMarketDataProvider
from app.options.paper_trading.cost_calculator import IndianDerivativesCostCalculator

SCRATCH_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
LIVE_TRADE_LOG_FILE = os.path.join(SCRATCH_DIR, "live_paper_trade_log.json")

async def execute_live_paper_test(duration_seconds=30, interval_seconds=3):
    print("=" * 80)
    print("🚀 AIVOLVE v3.0 — LIVE MARKET PAPER TRADING EXECUTION & REAL-TIME MONITORING")
    print(f"Timestamp: {datetime.datetime.now(datetime.timezone.utc).isoformat()} UTC")
    print("Mode: STRICTLY PAPER_TRADING_ONLY (Zero Broker Order API, Zero Real Capital)")
    print("=" * 80)

    provider = AngelOneMarketDataProvider()
    cost_calc = IndianDerivativesCostCalculator()

    # Step 1: Fetch Live Spot & Index Quote
    print("\n[STEP 1] Fetching Live Spot Quote from Angel One SmartAPI...")
    nifty_quote = await provider.get_index_quote("NIFTY")
    spot_ltp = nifty_quote.get("ltp")
    day_high = nifty_quote.get("high")
    day_low = nifty_quote.get("low")
    spot_ts = nifty_quote.get("timestamp")
    print(f"  ✅ NIFTY 50 Spot LTP : ₹{spot_ltp:.2f}")
    print(f"     Day Range        : ₹{day_low:.2f} — ₹{day_high:.2f}")
    print(f"     Data Status      : {nifty_quote.get('dataStatus')} (Provider: {nifty_quote.get('provider')})")

    # Step 2: Fetch Live ATM Option Contract Quote
    strike = round(spot_ltp / 50.0) * 50.0
    print(f"\n[STEP 2] Resolving ATM Option Contract for Strike {strike:.0f} CE...")
    opt_quote = await provider.get_option_quote("NIFTY", strike, "CE")
    if not opt_quote:
        print("  ❌ Failed to fetch option quote. Fallback to 25200 CE...")
        opt_quote = await provider.get_option_quote("NIFTY", 25200.0, "CE")

    symbol = opt_quote.get("instrument")
    token = opt_quote.get("instrumentToken")
    lot_size = opt_quote.get("lotSize", 65)
    live_ltp = float(opt_quote.get("ltp", 0.0))
    bid = float(opt_quote.get("bid", live_ltp))
    ask = float(opt_quote.get("ask", live_ltp))
    volume = opt_quote.get("volume", 0)
    oi = opt_quote.get("openInterest", 0)
    market_ts = opt_quote.get("marketTimestamp")

    print(f"  ✅ Contract Symbol   : {symbol} (Token: {token})")
    print(f"     Expiry           : {opt_quote.get('expiry')}")
    print(f"     Exchange         : {opt_quote.get('exchange')}")
    print(f"     Lot Size         : {lot_size}")
    print(f"     GENUINE LIVE LTP : ₹{live_ltp:.2f}")
    print(f"     Bid / Ask        : ₹{bid:.2f} / ₹{ask:.2f} (Spread: ₹{ask - bid:.2f})")
    print(f"     Volume / OI      : {volume:,} / {oi:,}")
    print(f"     Market Timestamp : {market_ts}")

    if live_ltp <= 0:
        print("  ❌ Live LTP is 0. Cannot open paper trade.")
        return

    # Step 3: Open Simulated Paper Trade
    print("\n[STEP 3] Executing Simulated BUY Paper Trade...")
    qty = lot_size * 1  # 1 lot
    entry_price = live_ltp
    trade_value = entry_price * qty
    sl = round(entry_price * 0.80, 2)  # 20% SL (~₹18-20 pts)
    target_1 = round(entry_price * 1.25, 2)  # 25% target (~₹23 pts)
    target_2 = round(entry_price * 1.50, 2)  # 50% target

    entry_costs = cost_calc.calculate_option_transaction_costs(
        transaction_type="BUY",
        premium=entry_price,
        quantity=qty,
        strike=strike
    )

    trade_id = f"LIVE-PAPER-{int(time.time())}"
    opened_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")

    paper_position = {
        "tradeId": trade_id,
        "instrument": "NIFTY",
        "symbol": symbol,
        "token": token,
        "optionType": "CE",
        "strike": strike,
        "side": "BUY",
        "lots": 1,
        "quantity": qty,
        "entryPrice": entry_price,
        "entryValue": trade_value,
        "stopLoss": sl,
        "target1": target_1,
        "target2": target_2,
        "entryCosts": entry_costs,
        "openedAt": opened_at,
        "status": "OPEN",
        "provenance": "GENUINE_ANGEL_ONE_LIVE_MARKET",
        "ticks": []
    }

    print(f"  📝 Trade ID         : {trade_id}")
    print(f"     Side             : BUY (Long Option)")
    print(f"     Quantity         : {qty} (1 Lot)")
    print(f"     Executed Fill    : ₹{entry_price:.2f} (Exact Live Market LTP)")
    print(f"     Position Value   : ₹{trade_value:,.2f}")
    print(f"     Stop-Loss        : ₹{sl:.2f} (-{entry_price - sl:.2f} pts | -₹{(entry_price - sl) * qty:,.2f})")
    print(f"     Target 1         : ₹{target_1:.2f} (+{target_1 - entry_price:.2f} pts | +₹{(target_1 - entry_price) * qty:,.2f})")
    print(f"     Estimated Costs  : ₹{entry_costs.get('totalCharges', 0):.2f} (STT: ₹{entry_costs.get('stt', 0):.2f}, Exch: ₹{entry_costs.get('exchangeTurnoverCharges', 0):.2f}, GST: ₹{entry_costs.get('gst', 0):.2f})")

    # Step 4: Real-Time Live Market Tick Progression
    print("\n[STEP 4] Monitoring Real-Time Live Market Ticks...")
    print("-" * 80)
    print(f"{'Time':<12} | {'Spot LTP':<10} | {'Opt LTP':<9} | {'Chg (pts)':<10} | {'Gross P&L':<12} | {'Net P&L':<12} | {'Status'}")
    print("-" * 80)

    start_time = time.time()
    tick_count = 0
    max_favorable_excursion = 0.0
    max_adverse_excursion = 0.0
    last_quote = opt_quote

    while time.time() - start_time < duration_seconds:
        tick_count += 1
        now_str = datetime.datetime.now().strftime("%H:%M:%S")

        try:
            # Poll fresh live quote
            fresh_opt = await provider.get_option_quote("NIFTY", strike, "CE")
            fresh_spot = await provider.get_index_quote("NIFTY")
            current_spot_ltp = fresh_spot.get("ltp", spot_ltp)
            current_opt_ltp = float(fresh_opt.get("ltp", entry_price))
            last_quote = fresh_opt
        except Exception as e:
            current_opt_ltp = entry_price
            current_spot_ltp = spot_ltp

        # Calculations
        pts_diff = current_opt_ltp - entry_price
        gross_pnl = pts_diff * qty
        
        # Estimate exit cost for net P&L
        exit_costs = cost_calc.calculate_option_transaction_costs(
            transaction_type="SELL",
            premium=current_opt_ltp,
            quantity=qty,
            strike=strike
        )
        total_costs = entry_costs.get("totalCharges", 0.0) + exit_costs.get("totalCharges", 0.0)
        net_pnl = gross_pnl - total_costs

        if pts_diff > max_favorable_excursion:
            max_favorable_excursion = pts_diff
        if pts_diff < max_adverse_excursion:
            max_adverse_excursion = pts_diff

        status = "IN_RANGE"
        if current_opt_ltp >= target_1:
            status = "🎯 TARGET 1 HIT"
        elif current_opt_ltp <= sl:
            status = "🛑 SL TRIGGERED"

        gross_str = f"+₹{gross_pnl:,.2f}" if gross_pnl >= 0 else f"-₹{abs(gross_pnl):,.2f}"
        net_str = f"+₹{net_pnl:,.2f}" if net_pnl >= 0 else f"-₹{abs(net_pnl):,.2f}"
        pts_str = f"+{pts_diff:.2f}" if pts_diff >= 0 else f"{pts_diff:.2f}"

        print(f"{now_str:<12} | ₹{current_spot_ltp:<9.2f} | ₹{current_opt_ltp:<8.2f} | {pts_str:<10} | {gross_str:<12} | {net_str:<12} | {status}")

        paper_position["ticks"].append({
            "timestamp": datetime.datetime.now().isoformat(),
            "spotLtp": current_spot_ltp,
            "optionLtp": current_opt_ltp,
            "ptsDiff": pts_diff,
            "grossPnl": gross_pnl,
            "netPnl": net_pnl,
            "volume": fresh_opt.get("volume")
        })

        if status != "IN_RANGE":
            print(f"\n⚡ Event Triggered: {status} at LTP ₹{current_opt_ltp:.2f}!")
            break

        await asyncio.sleep(interval_seconds)

    print("-" * 80)
    print("\n[STEP 5] Live Paper Trade Summary:")
    print(f"  Total Monitoring Duration : {int(time.time() - start_time)} seconds ({tick_count} live polls)")
    print(f"  Entry Fill Price         : ₹{entry_price:.2f}")
    print(f"  Final Observed LTP       : ₹{paper_position['ticks'][-1]['optionLtp']:.2f}")
    final_pts = paper_position['ticks'][-1]['ptsDiff']
    final_gross = paper_position['ticks'][-1]['grossPnl']
    final_net = paper_position['ticks'][-1]['netPnl']
    print(f"  Final Points Move        : {'+' if final_pts >= 0 else ''}{final_pts:.2f} pts")
    print(f"  Final Gross P&L          : {'+' if final_gross >= 0 else ''}₹{final_gross:,.2f}")
    print(f"  Final Net P&L (Post-Tax) : {'+' if final_net >= 0 else ''}₹{final_net:,.2f}")
    print(f"  Max Favorable Excursion  : +{max_favorable_excursion:.2f} pts (+₹{max_favorable_excursion * qty:,.2f})")
    print(f"  Max Adverse Excursion    : {max_adverse_excursion:.2f} pts (-₹{abs(max_adverse_excursion) * qty:,.2f})")

    # Persist in scratch records
    with open(LIVE_TRADE_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(paper_position, f, indent=2)
    print(f"\n  💾 Live trade telemetry saved to: {LIVE_TRADE_LOG_FILE}")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(execute_live_paper_test(duration_seconds=30, interval_seconds=3))

