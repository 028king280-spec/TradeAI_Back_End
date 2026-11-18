with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\data\market_calendar.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for i in range(25, 95):
    print(f'{i+1}: {lines[i]}')
