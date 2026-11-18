with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\options\paper_trading\paper_engine.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if 'def _load_state' in line or 'def __init__' in line:
            print(''.join(lines[i:i+35]))

