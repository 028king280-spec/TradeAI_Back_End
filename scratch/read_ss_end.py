with open(r'd:\ReactJs\aivolve-trading-ai\backend\app\options\setup_selector.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
print(f'Total lines: {len(lines)}')
for i in range(len(lines)-30, len(lines)):
    print(f'{i+1}: {lines[i]}')
