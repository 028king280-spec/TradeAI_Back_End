with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\options\next_session_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
print('=== Lines 179-195 ===')
for i in range(178, 195):
    print(f'{i+1}: {lines[i]}')

print('=== Lines 330-340 ===')
for i in range(329, 340):
    print(f'{i+1}: {lines[i]}')
