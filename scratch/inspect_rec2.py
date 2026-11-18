import sys
sys.path.append(r'd:\ReactJs\aivolve-trading-ai\backend')

from app.options.next_session_engine import evaluate_next_session_recommendation

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
print('hasQualifiedRecommendation:', rec2['hasQualifiedRecommendation'])
print('recommendation:', rec2['recommendation'])
print('decision:', rec2['decision'])
