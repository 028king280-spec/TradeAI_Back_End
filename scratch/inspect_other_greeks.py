import os

base_dir = r'd:\ReactJs\aivolve-trading-ai\backend'
files = [
    'app\options\pipeline_orchestrator.py',
    'app\options\setup_selector.py',
    'app\options\ict_smc\options_intelligence.py'
]

for rel in files:
    p = os.path.join(base_dir, rel)
    print(f'=== {rel} ===')
    with open(p, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            if 'greeks' in line.lower():
                for j in range(max(0, idx-2), min(len(lines), idx+8)):
                    print(f'  {j+1}: {lines[j].rstrip()}')
                print('---')
