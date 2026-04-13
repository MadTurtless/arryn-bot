from pathlib import Path
import os
from discord.ext import commands
from dotenv import load_dotenv, set_key

from utils.helper import build_embed, check_perms


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.hybrid_command()
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
        await new_msg.add_reaction("\U0001f7e2")
        await new_msg.add_reaction("\U0001F7E3")

        dotenv_path = Path(".env")
        set_key(dotenv_path,"REACTION_ROLES_MESSAGE_ID", str(new_msg.id))
        await ctx.send("Message sent successfully!")


async def setup(bot):
    await bot.add_cog(Commands(bot))
