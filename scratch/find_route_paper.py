import os

base_dir = r'd:\ReactJs\aivolve-trading-ai\backend\app\api\routes'
for f in os.listdir(base_dir):
    if f.endswith('.py'):
        p = os.path.join(base_dir, f)
        with open(p, 'r', encoding='utf-8') as fh:
            t = fh.read()
            if 'paper' in t.lower():
                print(f'Match in {f}')
