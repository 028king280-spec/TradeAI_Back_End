with open(r'd:\ReactJs\aivolve-trading-ai\backend\tests\test_options_platform.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for i, l in enumerate(lines):
    if 'test_next_session' in l:
        print(f'Line {i+1}: {l}')
        print('\n'.join(lines[i:i+40]))
        print('='*50)
