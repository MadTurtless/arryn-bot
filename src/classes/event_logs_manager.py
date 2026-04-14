import os
from discord.ext import commands
from dotenv import load_dotenv

from classes.database_manager import DatabaseManager
from utils.helper import parse_event_log

load_dotenv()

class EventLogsManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != int(os.getenv("EVENT_LOGS_CHANNEL_ID")):
            return

        if message.author.bot:
            return

        msg = message.content
        lines = msg.split("\n")
        log = parse_event_log(lines)
        log["division"] = "Arryn"
        log["msg_id"] = message.id
        db = DatabaseManager()
        db.add_event(log)

async def setup(bot):
    await bot.add_cog(EventLogsManager(bot))
