import subprocess

files = [
    'tests/test_feature_pipeline_phase5_2a.py',
    'tests/test_label_engine_phase5_2b.py',
    'tests/test_observation_engine_phase5_2c.py',
    'tests/test_monday_live_session_protocol.py',
    'tests/test_end_to_end_full_pipeline_phase_d.py',
    'tests/test_paper_trading_engine.py',
    'tests/test_p0_live_data_reliability.py'
]

total = 0
for f in files:
    out = subprocess.check_output(['.venv\\Scripts\\pytest', f, '--collect-only', '-q']).decode('utf-8')
    last_line = [line for line in out.strip().split('\n') if 'test' in line][-1]
    count = int(last_line.split()[0])
    total += count
    print(f"{f}: {count} tests ({last_line})")

print(f"\nTOTAL ACROSS ALL 7 FILES: {total}")

