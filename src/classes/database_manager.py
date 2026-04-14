import sqlite3

import discord

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect("data/db.sqlite")
        self.cursor = self.conn.cursor()
        pass

    def add_user(self, user: discord.User):
        query = "INSERT INTO users VALUES (?, 0)"

        self.cursor.execute(query, (user.id,))
        self.conn.commit()

    def get_user(self, user_id: int) -> discord.User:
        query = "SELECT * FROM users WHERE id = ?"

        user = self.cursor.execute(query, (user_id,))
        user = self.cursor.fetchone()
        return user