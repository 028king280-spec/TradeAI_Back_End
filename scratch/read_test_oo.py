with open(r'd:\ReactJs\aivolve-trading-ai\backend\tests\test_options_platform.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for i in range(165, 185):
    print(f'{i+1}: {lines[i]}')
