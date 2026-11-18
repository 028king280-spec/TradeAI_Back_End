with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\options\paper_trading\paper_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for i in range(310, 365):
    print(f'{i+1}: {lines[i]}')
