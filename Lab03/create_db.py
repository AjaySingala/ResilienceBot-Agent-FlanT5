import sqlite3
import os

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/incidents.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY,
    service TEXT,
    date TEXT,
    root_cause TEXT,
    impact TEXT,
    sla_breach INTEGER
)
""")

data = [
("payment", "2023-07-12", "Downstream banking API timeout", "Payment retries increased", 1),
("login", "2023-09-02", "Redis cache failure", "Users unable to login", 0),
("checkout", "2023-11-21", "Database connection pool exhaustion", "Checkout delays", 1),
("payment", "2023-12-03", "Gateway latency spike", "Slow payment processing", 0)
]

cursor.executemany(
"INSERT INTO incidents(service,date,root_cause,impact,sla_breach) VALUES(?,?,?,?,?)",
data
)

conn.commit()
conn.close()

print("Incident database created.")
