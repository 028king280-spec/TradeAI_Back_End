with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\options\paper_trading\paper_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
methods = re.findall(r'def\s+(\w+)\s*\(', text)
print('Methods in PaperTradingEngine:')
for m in methods[:25]:
    print(' ', m)

