with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\options\next_session_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
print(f'Total lines in next_session_engine.py: {len(lines)}')
