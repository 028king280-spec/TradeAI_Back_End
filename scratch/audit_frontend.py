import os, re

matches = []
src_dir = r"d:\ReactJs\aivolve-trading-ai\src"
for root, dirs, files in os.walk(src_dir):
    for f in files:
        if f.endswith((".ts", ".tsx", ".js", ".jsx")):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                txt = fh.read()
                for m in re.finditer(r"['\"`](/api)?/(options|signals)[^'\"`\s\)]*['\"`]", txt):
                    matches.append((p.replace(src_dir, "src"), m.group(0)))

for path, ep in sorted(set(matches)):
    print(f"{path}: {ep}")
