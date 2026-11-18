with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\options\greeks_risk_engine.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if 'def configure_policy' in line:
            print(''.join(lines[i:i+55]))
            break

