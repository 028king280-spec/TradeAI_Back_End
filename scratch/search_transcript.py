import json

transcript_path = r"C:\Users\Sourav Verma\.gemini\antigravity\brain\a47b88ae-3d04-471a-a671-adebd0b6ad2f\.system_generated\logs\transcript.jsonl"

found = []
try:
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            obj = json.loads(line)
            content = str(obj.get('content', ''))
            user_input = str(obj.get('thinking', ''))
            if 'phase 6' in content.lower() or 'phase 7' in content.lower() or 'phase 6' in user_input.lower() or 'phase 7' in user_input.lower():
                found.append((idx, obj.get('type'), obj.get('source'), content[:200]))
except Exception as e:
    print(f"Error: {e}")

print(f"Total transcript matches for Phase 6/7: {len(found)}")
for m in found:
    print(m)

