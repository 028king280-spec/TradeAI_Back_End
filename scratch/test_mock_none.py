import sys
from unittest.mock import patch
sys.path.append(r'd:\ReactJs\aivolve-trading-ai\backend')

from app.options.next_session_engine import evaluate_next_session_recommendation
from app.options.option_chain import generate_index_option_chain

chain = generate_index_option_chain('NIFTY 50', 24850.0, 50.0, filter_mode='ATM')

with patch('app.options.next_session_engine.calculate_black_scholes', return_value=None):
    rec = evaluate_next_session_recommendation(
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
    print('Recommendation with mocked calculate_black_scholes=None:')
    print('hasQualified:', rec['hasQualifiedRecommendation'])
    print('Greeks block:', rec['recommendation']['greeks'])
    assert rec['recommendation']['greeks']['gamma'] is None
    assert rec['recommendation']['greeks']['vega'] is None
    assert rec['recommendation']['greeks']['gamma'] != 0.0
    assert rec['recommendation']['greeks']['vega'] != 0.0
    print('Assertions passed!')
