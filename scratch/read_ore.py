with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\options\option_risk_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
print(f'Total lines: {len(lines)}')
print('First 120 lines:')
print('\n'.join(lines[:120]))
