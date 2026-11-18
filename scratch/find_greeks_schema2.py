import os

base_dir = r'd:\ReactJs\aivolve-trading-ai\backend'
app_dir = os.path.join(base_dir, 'app')
for root, dirs, files in os.walk(app_dir):
    for f in files:
        if f.endswith('.py'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                t = fh.read()
                if '"greeks":' in t or "'greeks':" in t:
                    rel = os.path.relpath(p, base_dir)
                    print(f'Match in {rel}')
