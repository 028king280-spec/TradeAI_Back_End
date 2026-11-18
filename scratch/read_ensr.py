with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\options\next_session_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for i, l in enumerate(lines):
    if 'def evaluate_next_session_recommendation' in l:
        print(f'Line {i+1}: {l}')
        print('\n'.join(lines[i:i+50]))
        break
