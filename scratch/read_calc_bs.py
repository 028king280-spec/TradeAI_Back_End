with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\options\greeks.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for i, l in enumerate(lines):
    if 'def calculate_black_scholes' in l:
        print(f'Line {i+1}: {l}')
        print('\n'.join(lines[i:i+60]))
        break
