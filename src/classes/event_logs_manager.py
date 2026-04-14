"""
Handles listening for event logs and parsing the data to hand off to the database manager.

Expected format:
    Event Type: [Type Name]
    Host: [@Mention]
    Participants: [@Mention1, @Mention2, ...]
    Proof: [Attached Image or Link]
Note: the proof line is ignored by the parser.
"""

import os
from discord.ext import commands
from dotenv import load_dotenv

from classes.database_manager import DatabaseManager
from utils.helper import parse_event_log

load_dotenv()

class EventLogsManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DatabaseManager()

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Listens for any message sent in the server.
        This is then filtered to only messages that are both not from the bot and in one of the specified channels.
        When a message meets these criteria, it is first split into multiple lines,
        then handed off to the helper to parse the data into a dictionary.
        """
        if message.author.bot:
            return

        channels = {
            int(os.getenv("ARRYN_LOG_CHANNEL_ID")): "Arryn",
            int(os.getenv("Knights_LOG_CHANNEL_ID")): "Knights",
            int(os.getenv("GUARDS_LOGS_CHANNEL_ID")): "Guards",
            int(os.getenv("CAVALRY_LOGS_CHANNEL_ID")): "Cavalry"
        }

        if message.channel.id not in channels:
            return

        msg = message.content
        lines = msg.split("\n")
        log = parse_event_log(lines)

        log["division"] = channels[message.channel.id]
        log["msg_id"] = message.id

        self.db.add_event(log)

async def setup(bot):
    await bot.add_cog(EventLogsManager(bot))
