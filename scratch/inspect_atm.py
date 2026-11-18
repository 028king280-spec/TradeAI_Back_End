with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\options\next_session_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for i in range(44, 75):
    print(f'{i+1}: {lines[i]}')
