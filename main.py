import discord
from dotenv import load_dotenv
import os
import logging

from src.classes.client import Client

load_dotenv()

token = os.getenv("DISCORD_TOKEN")
r_roles_msg_id = int(os.getenv("REACTION_ROLES_MESSAGE_ID"))

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

client = Client(intents=intents, r_roles_msg_id=r_roles_msg_id)

client.run(token)