"""
Handles listening for event logs and parsing the data to hand off to the database manager.

Expected format:
    Event Type: [Type Name]
    Host: [@Mention]
    Participants: [@Mention1, @Mention2, ...]
    Proof: [Attached Image or Link]
Note: the proof line is ignored by the parser.
"""
import asyncio
import os
import time

from discord.ext import commands
from dotenv import load_dotenv

from classes.database_manager import DatabaseManager
from utils.helper import parse_event_log

load_dotenv()

def validate_event_log(log):
    """
    Validates the log dict has the required keys.
    """
    required = ["type", "host_id", "participants"]
    return all(item in log for item in required)

class EventLogsManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DatabaseManager()
        self.channels = {
            int(os.getenv("ARRYN_LOGS_CHANNEL_ID")): "Arryn",
            int(os.getenv("KNIGHTS_LOGS_CHANNEL_ID")): "Knights",
            int(os.getenv("GUARDS_LOGS_CHANNEL_ID")): "Guards",
            int(os.getenv("CAVALRY_LOGS_CHANNEL_ID")): "Cavalry"
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Listens for any message sent in the server.
        This is then filtered to only messages that are both not from the bot and in one of the specified channels.
        When a message meets these criteria, it is first split into multiple lines,
        then handed off to the helper to parse the data into a dictionary.

        If the dictionary returns as invalid, an error message will be sent and it, along with the message, will self-destruct.
        """
        if message.author.bot:
            return

        if message.channel.id not in self.channels:
            return

        msg = message.content
        lines = msg.split("\n")
        log = parse_event_log(lines)

        if not validate_event_log(log):
            print("Invalid log")
            await message.reply("Invalid log. Please check the log and try again.", delete_after=5)
            await asyncio.sleep(10)
            await message.delete()
            return

        log["division"] = self.channels[message.channel.id]
        log["msg_id"] = message.id

        self.db.add_event(log)
        await message.add_reaction("\u2705")

async def setup(bot):
    await bot.add_cog(EventLogsManager(bot))
