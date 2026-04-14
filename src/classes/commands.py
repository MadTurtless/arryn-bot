"""
Registers commands for the bot
"""
from pathlib import Path
import os
from discord.ext import commands
from dotenv import load_dotenv, set_key

from src.utils.helper import build_embed, check_perms


async def add_reactions(msg):
    """
    This function acts as a helper to add reactions to a message.
    :param msg: discord.ext.commands.Message object
    :return: void
    """
    emojis = ["\U0001F1FF\U0001F1E6",   #South African Flag
              "\U0001F1E8\U0001F1F3",   #Chinese Flag
              "\U0001F1E6\U0001F1FA",   #Australian Flag
              "\U0001F1EA\U0001F1FA",   #European Flag
              "\U0001F1FA\U0001F1F8",   #United States Flag
              "\U0001F1E7\U0001F1F7"]   #Brazilian Flag
    for emoji in emojis:
        await msg.add_reaction(emoji)
    return


class Commands(commands.Cog):
    """
    The Commands class is a cog implementation that acts as a wrapper for generic commands.
    More specific functionalities can be found in their own classes.
    Note: This class modifies environment variables! Check that they're present if something breaks.
    """
    def __init__(self, bot):
        """
        :param bot: discord.ext.commands.Bot object
        """
        self.bot = bot

    @commands.hybrid_command(
        description="Send the embed message that will be used for reaction roles.")
    @check_perms()
    async def send_reaction_embed(self, ctx):
        """
        This function/command sends an embed message to a specific channel and adds reactions to it.
        These are then used to assign roles.
        :param ctx: discord.ext.commands.Context object
        :return: void
        """
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
        await ctx.send("Message sent successfully!")

        dotenv_path = Path(".env")
        set_key(dotenv_path,"REACTION_ROLES_MESSAGE_ID", str(new_msg.id))
"""
    @commands.hybrid_command()
    async def check_status(self, ctx):
        await ctx.send("This is the development version of Arryn Aid.\n"
                       "-# Not intended for public use.")
"""

async def setup(bot):
    """
    This function adds all the commands to the bot.
    :param bot: discord.ext.commands.Bot object
    :return: void
    """
    await bot.add_cog(Commands(bot))
