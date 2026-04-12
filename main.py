import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print(f"Synced slash commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    print(f"Logged in as {bot.user}")

@bot.hybrid_command()
async def hello(ctx):
    await ctx.send('Hello!')

bot.run(token)