with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\options\greeks_risk_engine.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if 'skip_governance_registry_check' in line:
            print(''.join(lines[i:i+40]))
            break

