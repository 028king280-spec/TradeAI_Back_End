with open(r'd:\ReactJs\aivolve-trading-ai\AIVOLVE_MASTER_COMPLETION_ROADMAP.md', 'r', encoding='utf-8') as f:
    text = f.read()
lines = text.split('\n')
for i, l in enumerate(lines):
    if 'phase 7' in l.lower() or 'engine 10' in l.lower() or 'dynamic risk' in l.lower():
        start = max(0, i - 5)
        end = min(len(lines), i + 25)
        print(f"--- Roadmap line {i} ---")
        print('\n'.join(lines[start:end]))
        print('='*40)
