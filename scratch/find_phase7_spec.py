import json
import re

transcript_path = r"C:\Users\Sourav Verma\.gemini\antigravity\brain\a47b88ae-3d04-471a-a671-adebd0b6ad2f\.system_generated\logs\transcript_full.jsonl"
with open(transcript_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if "Engine 10" in line or "Phase 7" in line or "Dynamic Risk" in line:
            obj = json.loads(line)
            if obj.get("type") == "USER_INPUT":
                content = obj.get("content", "")
                if "Master Development Specification" in content or "Master Blueprint" in content or "Phase 07" in content or "Phase 7" in content:
                    print(f"Line {idx} (Step {obj.get('step_index')}):")
                    # Find mentions of Engine 10 or Phase 7
                    for match in re.finditer(r"(Phase\s*0?7[^\n]+|Engine\s*10[^\n]+)", content, re.IGNORECASE):
                        print("  ->", match.group(0))

