import os

base_dir = r'd:\ReactJs\aivolve-trading-ai\backend'
for root, dirs, files in os.walk(os.path.join(base_dir, 'app')):
    for f in files:
        if f.endswith('.py'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                t = fh.read()
                if 'PaperTradingEngine' in t:
                    rel = os.path.relpath(p, base_dir)
                    print(f'Match in {rel}')
