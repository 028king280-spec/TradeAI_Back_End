with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\options\paper_trading\paper_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
print('\n'.join(lines[580:720]))
