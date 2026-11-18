with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\options\next_session_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for i, l in enumerate(lines):
    if 'greeks' in l.lower() or 'black_scholes' in l.lower() or 'gamma' in l.lower() or 'vega' in l.lower():
        print(f'{i+1}: {l}')
