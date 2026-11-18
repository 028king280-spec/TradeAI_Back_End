import os

terms = ['phase 6', 'phase 7']
matches = []

for root, dirs, files in os.walk('..'):
    dirs[:] = [d for d in dirs if d not in ['.venv', 'node_modules', '.git', '.next', '__pycache__']]
    for f in files:
        if f.endswith(('.md', '.py', '.ts', '.tsx', '.json', '.txt')):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                    for i, line in enumerate(fp, 1):
                        for t in terms:
                            if t in line.lower():
                                matches.append((t, path, i, line.strip()))
            except Exception:
                pass

print(f"Total Phase 6/7 matches: {len(matches)}")
for t, path, i, line in matches:
    print(f"[{t}] {path}:{i} -> {line}")
