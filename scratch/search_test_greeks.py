import os

test_dir = r'd:\ReactJs\aivolve-trading-ai\backend\tests'
for fname in os.listdir(test_dir):
    if fname.endswith('.py'):
        fpath = os.path.join(test_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'gamma' in content or 'vega' in content or 'next_session' in content or 'calculate_black_scholes' in content:
                print(f'Match in {fname}')
