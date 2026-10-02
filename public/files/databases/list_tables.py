import sqlite3

con = sqlite3.connect("data/Library.db")
for (name,) in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    cols = [row[1] for row in con.execute(f"PRAGMA table_info({name})")]
    print(f"{name}: {', '.join(cols)}")
