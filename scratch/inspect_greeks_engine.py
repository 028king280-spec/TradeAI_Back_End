import re

with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\options\greeks_risk_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

print('Classes in greeks_risk_engine.py:')
for c in re.findall(r'class\s+(\w+)', text):
    print(' ', c)

print('\nFunctions/Methods:')
for m in re.findall(r'def\s+(\w+)\s*\(', text):
    print(' ', m)

