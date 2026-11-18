import json

transcript_path = r"C:\Users\Sourav Verma\.gemini\antigravity\brain\a47b88ae-3d04-471a-a671-adebd0b6ad2f\.system_generated\logs\transcript_full.jsonl"
with open(transcript_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i == 4600:
            data = json.loads(line)
            content = data.get("content", "")
            lines = content.split('\n')
            for idx, l in enumerate(lines):
                if any(w in l.lower() for w in ["engine 10", "phase 7", "phase 07", "dynamic risk"]):
                    start = max(0, idx - 5)
                    end = min(len(lines), idx + 25)
                    print(f"--- Line 4600 Match around line {idx} ---")
                    print("\n".join(lines[start:end]))
                    print("="*40)
