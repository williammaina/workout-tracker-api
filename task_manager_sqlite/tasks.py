import sqlite3

def get_all_tasks():
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        return cursor.fetchall()

def get_task_by_id(task_id):
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        # Use ? placeholders — never f-strings!
        cursor.execute(
            'SELECT * FROM tasks WHERE id=?',
            (task_id,))
        return cursor.fetchone()

def get_incomplete_tasks():
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM tasks WHERE completed=0'
            ' ORDER BY created_at DESC')
        return cursor.fetchall()