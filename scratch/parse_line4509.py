import json

transcript_path = r"C:\Users\Sourav Verma\.gemini\antigravity\brain\a47b88ae-3d04-471a-a671-adebd0b6ad2f\.system_generated\logs\transcript_full.jsonl"
with open(transcript_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i == 4509:
            data = json.loads(line)
            content = data.get("content", "")
            print(f"Content length: {len(content)}")
            # Let's search for 'Engine 10' or 'Risk Management' or 'Dynamic Risk'
            lines = content.split('\n')
            for idx, l in enumerate(lines):
                if any(k in l.lower() for k in ["engine 10", "risk management", "capital defense", "dynamic risk", "phase 7", "drawdown", "exposure"]):
                    start = max(0, idx - 5)
                    end = min(len(lines), idx + 25)
                    print(f"--- Match around line {idx} ---")
                    print("\n".join(lines[start:end]))
                    print("="*40)
