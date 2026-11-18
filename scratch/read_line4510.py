import json

transcript_path = r"C:\Users\Sourav Verma\.gemini\antigravity\brain\a47b88ae-3d04-471a-a671-adebd0b6ad2f\.system_generated\logs\transcript.jsonl"

with open(transcript_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if idx in range(4505, 4515):
            obj = json.loads(line)
            print(f"--- Line {idx} Type: {obj.get('type')} Source: {obj.get('source')} ---")
            content = obj.get('content', '')
            print(content[:1500])

