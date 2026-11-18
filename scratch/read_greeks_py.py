with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\options\greeks.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
print(f'Total lines: {len(lines)}')
print('\n'.join(lines[:60]))
