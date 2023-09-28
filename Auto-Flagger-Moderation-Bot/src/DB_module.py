import sqlite3

class DatabaseManager:
    def __init__(self, database_name='reddit_bot.db'):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                comment_id INTEGER PRIMARY KEY,
                username TEXT,
                comment_text TEXT,
                relevance_score INTEGER,
                toxicity_score INTEGER,
                spam_score INTEGER,
                breaks_rules_score INTEGER,
                total_score INTEGER
            )
        ''')
        self.conn.commit()

    def create_comment(self, comment_data):
        self.cursor.execute('''
            INSERT INTO comments (comment_text, username, toxicity_score)
            VALUES (?, ?, ?)
        ''', comment_data)
        self.conn.commit()

    def create_user(self, username, total_score):
        self.cursor.execute('''
            INSERT INTO users (username, total_score)
            VALUES (?, ?)
        ''', (username, total_score))
        self.conn.commit()

    def update_user_score(self, username, new_score):
        self.cursor.execute('''
            UPDATE users
            SET total_score = ?
            WHERE username = ?
        ''', (new_score, username))
        self.conn.commit()

    def get_user_score(self, username):
        self.cursor.execute('''
            SELECT total_score
            FROM users
            WHERE username = ?
        ''', (username,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return 0

    def list_comments(self):
        self.cursor.execute('SELECT * FROM comments')
        return self.cursor.fetchall()

    def list_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()