import os

for root, dirs, files in os.walk(r'd:\ReactJs\aivolve-trading-ai\backend\app'):
    for f in files:
        if f.endswith('.py'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                t = fh.read()
                if '\"greeks\":' in t or '\'greeks\':' in t:
                    print(f'Match in {os.path.relpath(p, r\"d:\ReactJs\aivolve-trading-ai\backend\")}')
