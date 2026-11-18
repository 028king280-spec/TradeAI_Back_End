with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\data\market_calendar.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for i, l in enumerate(lines):
    if 'def ' in l:
        print(f'{i+1}: {l}')
