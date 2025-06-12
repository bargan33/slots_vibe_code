import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = 'casino.db'

def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_db() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            balance INTEGER DEFAULT 100
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS stats (
            user_id INTEGER,
            spins INTEGER DEFAULT 0,
            total_won INTEGER DEFAULT 0,
            most_played_game TEXT DEFAULT 'slots',
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
        db.commit()

def create_user(username, password):
    with get_db() as db:
        try:
            db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                       (username, generate_password_hash(password)))
            db.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def verify_user(username, password):
    with get_db() as db:
        cur = db.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row and check_password_hash(row[1], password):
            return row[0]  # return user ID
        return None

def get_user_by_id(user_id):
    with get_db() as db:
        cur = db.execute("SELECT id, username, balance FROM users WHERE id = ?", (user_id,))
        return cur.fetchone()

def update_balance(user_id, amount):
    with get_db() as db:
        db.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, user_id))
        db.commit()

def record_spin(user_id, win_amount):
    with get_db() as db:
        cur = db.execute("SELECT user_id FROM stats WHERE user_id = ?", (user_id,))
        if cur.fetchone():
            db.execute("UPDATE stats SET spins = spins + 1, total_won = total_won + ? WHERE user_id = ?",
                       (win_amount, user_id))
        else:
            db.execute("INSERT INTO stats (user_id, spins, total_won) VALUES (?, 1, ?)",
                       (user_id, win_amount))
        db.commit()

def get_leaderboard():
    with get_db() as db:
        cur = db.execute("SELECT username, balance FROM users ORDER BY balance DESC LIMIT 10")
        return cur.fetchall()
    

def top_up_balance(user_id, amount):
    db = get_db()
    db.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, user_id))
    db.commit()
