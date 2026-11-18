import sqlite3

con = sqlite3.connect(r'd:\ReactJs\aivolve-trading-ai\backend\app\data\governance_ledger.db')
cur = con.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print('Tables in governance_ledger.db:', tables)
for t in tables:
    count = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"Table {t}: {count} rows")
    for r in cur.execute(f"SELECT * FROM {t} LIMIT 3").fetchall():
        print(' ', r)

