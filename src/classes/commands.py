from pathlib import Path
import os
from discord.ext import commands
from dotenv import load_dotenv, set_key

from src.utils.helper import build_embed, check_perms


async def add_reactions(msg):
    emojis = ["\U0001F1E6\U0001F1FA", #Australian Flag
              "\U0001F1E7\U0001F1F7", #Brazilian Flag
              "\U0001F1E8\U0001F1F3", #Chinese Flag
              "\U0001F1EA\U0001F1FA", #European Flag
              "\U0001F1FF\U0001F1E6", #South African Flag
              "\U0001F1FA\U0001F1F8"] #United States Flag
    for emoji in emojis:
        await msg.add_reaction(emoji)
    return


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.hybrid_command(description="Send the embed message that will be used for reaction roles.")
    @check_perms()
    async def send_reaction_embed(self, ctx):
        load_dotenv(override=True)
        stored_msg_id = os.getenv("REACTION_ROLES_MESSAGE_ID")

        guild = ctx.guild
        channel = guild.get_channel(int(os.getenv("REACTION_ROLES_CHANNEL_ID")))

        async for msg in channel.history():
            if msg.author == channel.guild.me:
                if msg.id == int(stored_msg_id):
                    await ctx.send("Message already exists!")
                    return

        new_msg = await channel.send(embed=await build_embed())
        await add_reactions(new_msg)

        dotenv_path = Path(".env")
        set_key(dotenv_path,"REACTION_ROLES_MESSAGE_ID", str(new_msg.id))
        await ctx.send("Message sent successfully!")


async def setup(bot):
    await bot.add_cog(Commands(bot))
