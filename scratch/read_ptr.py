import json

p = r'd:\ReactJs\aivolve-trading-ai\backend\app\data\paper_trading_records.json'
with open(p, 'r', encoding='utf-8') as f:
    data = json.load(f)

print('Keys:', list(data.keys()))
print('Balance:', data.get('balance'))
print('Open positions:', len(data.get('openPositions', [])))
print('Closed trades:', len(data.get('closedTrades', [])))
if data.get('closedTrades'):
    print('First closed trade keys:', list(data['closedTrades'][0].keys()))
    print('First closed trade exit timestamp:', data['closedTrades'][0].get('exitTimestamp'))
    print('First closed trade netPnl:', data['closedTrades'][0].get('netPnl'))
