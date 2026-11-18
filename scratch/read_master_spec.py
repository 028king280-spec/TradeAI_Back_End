import json

transcript_path = r"C:\Users\Sourav Verma\.gemini\antigravity\brain\a47b88ae-3d04-471a-a671-adebd0b6ad2f\.system_generated\logs\transcript_full.jsonl"
with open(transcript_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if idx == 4509:
            obj = json.loads(line)
            content = obj.get("content", "")
            print("=== LINE 4509 CONTENT ===")
            print(content)
            break

