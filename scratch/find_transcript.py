import json

transcript_path = r"C:\Users\Sourav Verma\.gemini\antigravity\brain\a47b88ae-3d04-471a-a671-adebd0b6ad2f\.system_generated\logs\transcript.jsonl"
with open(transcript_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if "Engine 10" in line or "Phase 07" in line or "Dynamic Risk Management" in line or "Phase 7" in line:
            print(f"Line {i}")
