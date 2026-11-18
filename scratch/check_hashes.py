import hashlib
import os

files = {
    'aivolve_trading.db': r'd:\ReactJs\aivolve-trading-ai\backend\aivolve_trading.db',
    'governance_ledger.db': r'd:\ReactJs\aivolve-trading-ai\backend\app\data\governance_ledger.db',
    'paper_trading_records.json': r'd:\ReactJs\aivolve-trading-ai\backend\app\data\paper_trading_records.json',
    'ml_trade_dataset.json': r'd:\ReactJs\aivolve-trading-ai\backend\app\data\ml_trade_dataset.json',
    'what_ai_learned.json': r'd:\ReactJs\aivolve-trading-ai\backend\app\data\what_ai_learned.json',
    'ml_strategy_weights.json': r'd:\ReactJs\aivolve-trading-ai\backend\app\data\ml_strategy_weights.json',
}

expected = {
    'aivolve_trading.db': 'C85C49BE76DEE40557C4B9AAF308B4E3BEACA03CD4B1CD1CE90D051566EABF44',
    'governance_ledger.db': '4B12B3BAB44BF913F15174278B346FA321D5C473272E40F8B7E6E2350034488E',
    'paper_trading_records.json': '00F968EF85095EB7C1DE336A1780F9EDE417426A253AC531446BEF1117DA0298',
    'ml_trade_dataset.json': '87EEA8802835BB4F5A0AD1D598F2CEC561C6D5237F123B8B57CD79BBBE2E6445',
    'what_ai_learned.json': '3ED015726DFF309000EEC473AB660F34E3BD4EFAEDCBE183B14D62C572E5CCC5',
    'ml_strategy_weights.json': 'C3C495F36214BD7FA58DDCA3C7F0280C14E15EB08DF41F868704F724C2A4E2FC',
}

all_match = True
for name, p in files.items():
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest().upper()
    exp = expected[name]
    match = (h == exp)
    if not match: all_match = False
    print(f'{name}: match={match} hash={h}')

print(f'ALL MATCH: {all_match}')
