import json
import re

transcript_path = r"C:\Users\Sourav Verma\.gemini\antigravity\brain\a47b88ae-3d04-471a-a671-adebd0b6ad2f\.system_generated\logs\transcript_full.jsonl"
with open(transcript_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if "Phase 07" in line or "Phase 7" in line or "Engine 10" in line:
            obj = json.loads(line)
            content = obj.get("content", "")
            # Look for sections describing Phase 7 or Engine 10
            matches = re.findall(r"(?:Phase\s*0?7|Engine\s*10)[^\n]{0,100}\n(?:[^\n]+\n){1,15}", content, re.IGNORECASE)
            if matches:
                print(f"--- Line {idx} (Type: {obj.get('type')}) ---")
                for m in matches[:3]:
                    print(m)
                    print("="*40)

