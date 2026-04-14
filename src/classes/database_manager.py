"""
Handles interaction between the bot and the database.
Important: All database actions should go through this class. No SQL in other files!
"""

import sqlite3

import discord

class DatabaseManager:
    def __init__(self):
        """
        Sets up the sqlite3 database connection.
        """
        self.conn = sqlite3.connect("data/db.sqlite")
        self.cursor = self.conn.cursor()
        pass

    def add_user(self, user_id: int):
        """
        Adds a user using its id.
        """
        query = "INSERT INTO users VALUES (?, 0)"

        try:
            self.cursor.execute(query, (user_id,))
            self.conn.commit()
            return 1
        except Exception as e:
            print(e)
            return -1

    def get_user(self, user_id: int):
        """
        Get a user's database entry from its id.
        """
        query = "SELECT * FROM users WHERE id = ?"

        self.cursor.execute(query, (user_id,))
        user = self.cursor.fetchone()
        return user

    def add_event_participants(self, participants):
        """
        Adds a list of participants to the event_participants table using their ids.
        If a user isn't yet known, it will also be added here.
        """
        query = "SELECT id FROM events"
        res = self.cursor.execute(query)
        event_id = res.fetchone()[-1]

        for p_id in participants:
            if not self.get_user(p_id):
                self.add_user(p_id)

            query = "INSERT INTO event_participants(event_id, user_id) VALUES (?, ?)"
            self.cursor.execute(query, (event_id, p_id))
            query = "UPDATE users SET nr_events_attended = nr_events_attended + 1 WHERE id = ?"
            self.cursor.execute(query, (p_id,))
        self.conn.commit()

    def add_event(self, event):
        """
        Adds an event to the events table.
        This function also calls the add_event_participants function.
        Expected format for the event dict:
        {
        "division": string,
        "type": string,
        "host_id": int,
        "participants": list of integers,
        "timestamp": datetime,
        "msg_id": int,
        }
        """
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
        """
        Get an event's database entry from its id.
        """
        query = "SELECT * FROM events WHERE id = ?"

        try:
            self.cursor.execute(query, (event_id,))
            event = self.cursor.fetchone()
            return event
        except Exception as e:
            print(e)
            return -1

    def get_events_by_user(self, user_id: int):
        """
        Get all events by a user's id.
        """
        query = "SELECT * FROM event_participants WHERE user_id = ?"

        try:
            self.cursor.execute(query, (user_id,))
            events = self.cursor.fetchall()
            return events
        except Exception as e:
            print(e)
            return -1
