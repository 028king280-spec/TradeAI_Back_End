with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\options\next_session_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
start = max(0, 315)
end = min(len(lines), 355)
for i in range(start, end):
    print(f'{i+1}: {lines[i]}')
