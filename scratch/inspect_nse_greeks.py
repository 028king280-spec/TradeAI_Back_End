with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\options\next_session_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
print('=== Lines 170-220 ===')
for i in range(169, 220):
    print(f'{i+1}: {lines[i]}')

print('=== Lines 325-345 ===')
for i in range(324, 345):
    print(f'{i+1}: {lines[i]}')
