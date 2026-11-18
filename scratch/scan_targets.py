import json

transcript_path = r"C:\Users\Sourav Verma\.gemini\antigravity\brain\a47b88ae-3d04-471a-a671-adebd0b6ad2f\.system_generated\logs\transcript_full.jsonl"
targets = [4600, 19498, 19503, 19536, 19538, 19539, 19540, 19544, 19550, 19558, 19562, 19567, 19581, 19653, 19654, 19655, 19738, 19781, 19883, 19884, 19909, 19910, 19912, 19915, 19917, 19921, 19925, 19926, 19929, 19939, 19941, 19943, 19945]

with open(transcript_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i in targets:
            data = json.loads(line)
            src = data.get("source", "")
            tp = data.get("type", "")
            content = data.get("content", "")
            print(f"=== Line {i} ({src} - {tp}) len={len(content)} ===")
            lines = content.split('\n')
            for l in lines:
                if any(w in l.lower() for w in ["phase 7", "phase 07", "engine 10", "dynamic risk", "capital defense"]):
                    print("  ", l[:120])
