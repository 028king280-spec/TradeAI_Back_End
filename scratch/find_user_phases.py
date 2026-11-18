import json

transcript_path = r"C:\Users\Sourav Verma\.gemini\antigravity\brain\a47b88ae-3d04-471a-a671-adebd0b6ad2f\.system_generated\logs\transcript.jsonl"

user_phase_prompts = []
with open(transcript_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        obj = json.loads(line)
        if obj.get('source') == 'USER_EXPLICIT':
            content = obj.get('content', '')
            if 'phase' in content.lower():
                user_phase_prompts.append((idx, content[:300].replace('\n', ' ')))

print(f"Total user prompts mentioning phase: {len(user_phase_prompts)}")
for idx, snippet in user_phase_prompts:
    print(f"Line {idx}: {snippet}")

