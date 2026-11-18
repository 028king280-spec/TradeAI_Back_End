import sys
sys.path.append(r'd:\ReactJs\aivolve-trading-ai\backend')

from app.options.next_session_engine import evaluate_next_session_recommendation
from app.options.option_chain import generate_index_option_chain
from fastapi.testclient import TestClient
from app.main import app

# Let's inspect what happens currently vs with monkeypatched fix
chain = generate_index_option_chain('NIFTY 50', 24850.0, 50.0, filter_mode='ATM')

print('--- Test 1: Valid Greeks ---')
rec1 = evaluate_next_session_recommendation(
    symbol='NIFTY 50',
    underlying_ltp=24850.0,
    sentiment='BULLISH',
    sentiment_score=72,
    strikes_data=chain['strikes'],
    atr_14=120.0,
    daily_high=24920.0,
    daily_low=24780.0,
    daily_close=24800.0,
    daily_open=24810.0,
    iv=0.15,
    vix_value=13.5
)
print('Rec 1 greeks:', rec1['recommendation']['greeks'])

print('--- Test 2: calculate_black_scholes returns None (e.g. spot <= 0) ---')
try:
    rec2 = evaluate_next_session_recommendation(
        symbol='NIFTY 50',
        underlying_ltp=0.0,
        sentiment='BULLISH',
        sentiment_score=72,
        strikes_data=[],
        atr_14=120.0,
        daily_high=24920.0,
        daily_low=24780.0,
        daily_close=24800.0,
        daily_open=24810.0,
        iv=0.15,
        vix_value=13.5
    )
    print('Rec 2 greeks:', rec2['recommendation']['greeks'])
except Exception as e:
    print('Rec 2 exception:', type(e), e)
