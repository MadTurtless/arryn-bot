import asyncio
import os
import logging
import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(intents=intents, command_prefix="!")

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

    try:
        synced = await bot.tree.sync()
        print(f"{bot.user} has synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

async def main():
    async with bot:
        await bot.load_extension("src.classes.commands")
        await bot.load_extension("src.classes.reaction_roles")
        await bot.start(token)

asyncio.run(main())
