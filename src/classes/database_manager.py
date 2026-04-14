import sqlite3

import discord

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect("data/db.sqlite")
        self.cursor = self.conn.cursor()
        pass

    def add_user(self, user_id: int):
        query = "INSERT INTO users VALUES (?, 0)"

        try:
            self.cursor.execute(query, (user_id,))
            self.conn.commit()
            return 1
        except Exception as e:
            print(e)
            return -1

    def get_user(self, user_id: int) -> discord.User:
        query = "SELECT * FROM users WHERE id = ?"

        self.cursor.execute(query, (user_id,))
        user = self.cursor.fetchone()
        return user

    def add_event_participants(self, participants):
        query = "SELECT id FROM events"
        res = self.cursor.execute(query)
        event_id = res.fetchone()[-1]

        for p_id in participants:
            if not self.get_event(p_id):
                self.add_user(p_id)

            query = "INSERT INTO event_participants(event_id, user_id) VALUES (?, ?)"
            self.cursor.execute(query, (event_id, p_id))
            query = "UPDATE users SET nr_events_attended = nr_events_attended + 1 WHERE id = ?"
            self.cursor.execute(query, (p_id,))
        self.conn.commit()

    def add_event(self, event):
        event["participants"].append(event["host_id"])
        query = "INSERT INTO events(division, type, host_id, timestamp, msg_id) VALUES (?, ?, ?, ?, ?)"
        try:
            self.cursor.execute(query, (event["division"], event["type"], event["host_id"], event["timestamp"], event["msg_id"]))
            self.add_event_participants(event["participants"])
            self.conn.commit()
            return 1
        except Exception as e:
            print(e)
            return -1

    def get_event(self, event_id: int):
        query = "SELECT * FROM events WHERE id = ?"

        try:
            self.cursor.execute(query, (event_id,))
            event = self.cursor.fetchone()
            return event
        except Exception as e:
            print(e)
            return -1

    def get_events_by_user(self, user_id: int):
        query = "SELECT * FROM event_participants WHERE user_id = ?"

        try:
            self.cursor.execute(query, (user_id,))
            events = self.cursor.fetchall()
            return events
        except Exception as e:
            print(e)
            return -1
