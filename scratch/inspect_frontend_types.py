with open(r'd:\ReactJs\aivolve-trading-ai\src\types\options.ts', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for i, l in enumerate(lines):
    if 'greeks' in l.lower() or 'recommendation' in l.lower() or 'nextsession' in l.lower():
        print(f'{i+1}: {l}')
