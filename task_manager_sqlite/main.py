# =====================================================================
# FILE: main.py
# =====================================================================

# 1. First, we import your tools (this links tasks.py to this file)
import sqlite3
import tasks 

# 2. Next, your exact code block runs to interact with the database
# (Open a connection, get a cursor, run SQL)
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM tasks")

rows = cursor.fetchall()
for row in rows:
    print(row)

conn.commit() 
conn.close() 

# 3. Your context manager code block runs next
with sqlite3.connect('tasks.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    print(cursor.fetchall())

# 4. (Optional) Now the app can also use the functions from tasks.py
print(tasks.get_all_tasks())