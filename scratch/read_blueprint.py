import json

transcript_path = r"C:\Users\Sourav Verma\.gemini\antigravity\brain\a47b88ae-3d04-471a-a671-adebd0b6ad2f\.system_generated\logs\transcript_full.jsonl"
with open(transcript_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i in (4509, 4510):
            data = json.loads(line)
            content = data.get("content", "")
            print(f"=== LINE {i} ===")
            print(f"Type: {data.get('type')}, Source: {data.get('source')}")
            # print first 2000 chars of content
            print(content[:2500])
            print("...\n")
