import sqlite3

def init_db():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS achievements
                 (id TEXT PRIMARY KEY, name TEXT, description TEXT, unlocked INTEGER)''')
    conn.commit()
    conn.close()

def save_achievement(achievement_id, name, description, unlocked):
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO achievements (id, name, description, unlocked)
                 VALUES (?, ?, ?, ?)''', 
              (achievement_id, name, description, 1 if unlocked else 0))
    conn.commit()
    conn.close()

def load_achievements():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('SELECT * FROM achievements')
    rows = c.fetchall()
    achievements = {}
    for row in rows:
        achievements[row[0]] = {
            "name": row[1],
            "description": row[2],
            "unlocked": bool(row[3])
        }
    conn.close()
    return achievements
