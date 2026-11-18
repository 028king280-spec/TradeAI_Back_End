import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tests.test_contract_selector_step4 import build_mock_option_chain
from app.options.contract_selector import select_option_contract
from app.options.option_risk_engine import calculate_option_risk_plan

def main():
    print("=" * 70)
    print("  AIVOLVE QUANTITATIVE OPTIONS INTELLIGENCE ENGINE v3.0")
    print("  PHASE 2 - STEP 4.2 LIVE RUN DEMONSTRATION")
    print("=" * 70)

    # 1. NIFTY Bullish Breakout Setup (BUY_CE)
    spot = 24500.0
    chain = build_mock_option_chain("NIFTY", spot)
    setup_ce = {
        "action": "BUY_CE",
        "entry_price": spot,
        "stop_loss": 24420.0,
        "target_1": 24580.0,
        "target_2": 24680.0,
        "target_3": 24780.0,
    }

    print("\n[1] UNDERLYING INDEX TRADE SETUP:")
    print(f"  Index: NIFTY 50 | Spot Entry: Rs {spot}")
    print(f"  Structural Stop-Loss: Rs 24,420.00 (-80 pts)")
    print(f"  Target 1: Rs 24,580.00 (+80 pts)")
    print(f"  Target 2: Rs 24,680.00 (+160 pts)")
    print(f"  Target 3: Rs 24,780.00 (+240 pts)")

    # Contract Selection
    selected = select_option_contract(setup_ce, "NIFTY", spot, chain)
    print("\n[2] DETERMINISTIC CONTRACT SELECTION:")
    print(f"  Qualification Status : {selected['qualification_status']}")
    print(f"  Contract Symbol      : {selected['contract_symbol']}")
    print(f"  Strike Price         : Rs {selected['strike']} ({selected['moneyness']})")
    print(f"  Derived Strike Step  : Rs {selected['derived_strike_spacing']}")
    print(f"  Lot Size             : {selected['lot_size']} units (Tick: Rs {selected['tick_size']})")
    print(f"  Delta / Gamma        : {selected['delta']} / {selected['gamma']}")
    print(f"  Theta / Vega         : Rs {selected['theta']}/day / Rs {selected['vega']}/%")
    print(f"  Entry Premium (Ask)  : Rs {selected['entry_premium']}")
    print(f"  Quoted Bid           : Rs {selected['bid']}")
    print(f"  Analytical Midpoint  : Rs {selected['analytical_midpoint']}")
    print(f"  Bid-Ask Spread       : {selected['spread_pct']}%")

    # Option Risk Plan
    plan = calculate_option_risk_plan(
        setup_ce,
        selected,
        risk_config={
            "risk_budget_inr": 15000.0,
            "slippage_pts": 0.25,
            "min_reward_to_risk": 1.25,
        },
        available_capital=100000.0,
    )

    print("\n[3] NON-LINEAR BLACK-SCHOLES SCENARIO REPRICING:")
    print(f"  Risk Qualification   : {plan['qualification_status']}")
    print(f"  Option Entry Premium : Rs {plan['entry_premium']} (Fill Model: {plan['execution_assumptions']['entry_fill_model']})")
    print(f"  Option Stop-Loss     : Rs {plan['option_stop_loss']} (Exit Model: {plan['execution_assumptions']['exit_fill_model']})")
    print(f"  Risk Per Unit        : Rs {plan['risk_per_unit']}")
    print(f"  Risk Per Lot         : Rs {plan['risk_per_lot']}")
    print(f"  Option Target 1      : Rs {plan['option_target_1']} | RR_T1: {plan['reward_to_risk']['rr_t1']} (Qualified: {plan['reward_to_risk']['rr_t1_qualified']})")
    print(f"  Option Target 2      : Rs {plan['option_target_2']} | RR_T2: {plan['reward_to_risk']['rr_t2']} (Qualified: {plan['reward_to_risk']['rr_t2_qualified']})")
    print(f"  Option Target 3      : Rs {plan['option_target_3']} | RR_T3: {plan['reward_to_risk']['rr_t3']} (Qualified: {plan['reward_to_risk']['rr_t3_qualified']})")
    print(f"  Composite RR Status  : {'QUALIFIED' if plan['reward_to_risk']['composite_qualified'] else 'REJECTED'}")

    print("\n[4] POSITION SIZING & CAPITAL ALLOCATION:")
    print(f"  Position Sizing Status : {plan['position_sizing_status']}")
    print(f"  Allocated Lots         : {plan['allocated_lots']} lots ({plan['allocated_lots'] * plan['lot_size']} units)")
    print(f"  Total Capital Exposure : Rs {plan['total_premium_exposure']:,.2f}")
    print(f"  Maximum Potential Risk : Rs {plan['max_potential_risk']:,.2f}")

    print("\n[5] QUANTITATIVE AUDIT & EXECUTION ASSUMPTIONS:")
    print(f"  Friction Deduction     : Half-spread Rs {plan['execution_assumptions']['half_spread_deduction']} + Slippage Rs {plan['execution_assumptions']['additional_slippage_pts']}")
    print(f"  Double Counting Avoided: {plan['execution_assumptions']['double_counting_prevented']}")
    print(f"  Scenario Horizons      : SL: {plan['scenario_horizons']['stop_loss_minutes']}m | T1: {plan['scenario_horizons']['target_1_minutes']}m | T2: {plan['scenario_horizons']['target_2_minutes']}m (Status: {plan['scenario_horizons']['calibration_status']})")
    print(f"  IV Stress (SL Crush)   : Base {plan['iv_stress_model']['stop_loss']['base_iv_pct']}% -> Stressed {plan['iv_stress_model']['stop_loss']['stressed_iv_pct']}% ({plan['iv_stress_model']['stop_loss']['stress_pct']}% {plan['iv_stress_model']['stop_loss']['stress_interpretation']})")
    print("=" * 70)

if __name__ == "__main__":
    main()

