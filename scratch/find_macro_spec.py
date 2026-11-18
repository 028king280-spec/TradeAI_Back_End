import json

transcript_path = r"C:\Users\Sourav Verma\.gemini\antigravity\brain\a47b88ae-3d04-471a-a671-adebd0b6ad2f\.system_generated\logs\transcript_full.jsonl"

matches = []
with open(transcript_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if idx in [4509, 4510, 4524]:
            obj = json.loads(line)
            content = obj.get('content', '')
            for l in content.split('\n'):
                if any(k in l.lower() for k in ['macro', 'event', 'overnight', 'economic', 'engine 8', 'phase 6', 'phase 06']):
                    matches.append((idx, l.strip()))

for m in matches:
    print(m)

