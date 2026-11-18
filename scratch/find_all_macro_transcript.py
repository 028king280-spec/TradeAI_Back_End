import json

transcript_path = r"C:\Users\Sourav Verma\.gemini\antigravity\brain\a47b88ae-3d04-471a-a671-adebd0b6ad2f\.system_generated\logs\transcript_full.jsonl"

found = []
with open(transcript_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        obj = json.loads(line)
        content = obj.get('content', '')
        if 'macro and event' in content.lower() or 'overnight drift' in content.lower() or 'economic calendar' in content.lower():
            found.append((idx, obj.get('type'), obj.get('source'), [l.strip() for l in content.split('\n') if any(k in l.lower() for k in ['macro', 'event', 'overnight', 'economic'])]))

print(f"Total matching transcript entries: {len(found)}")
for idx, typ, src, lines in found[:20]:
    print(f"Line {idx} ({typ}, {src}):")
    for l in lines[:5]:
        print(f"   {l[:120]}")

