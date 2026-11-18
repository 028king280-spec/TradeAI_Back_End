import os

test_dir = r'd:\ReactJs\aivolve-trading-ai\backend\tests'
for fname in os.listdir(test_dir):
    if fname.endswith('.py'):
        fpath = os.path.join(test_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f):
                if 'greeks' in line.lower() and ('assert' in line or '==' in line or 'is ' in line):
                    print(f'{fname}:{idx+1} -> {line.strip()}')
