import os

from discord.ext import commands
from dotenv import load_dotenv

class ReactionRoles(commands.Cog):
    roles = {
        "\U0001F1E6\U0001F1FA": 1493250007061630986,  # Australian Flag
        "\U0001F1E7\U0001F1F7": 1493250050577399958,  # Brazilian Flag
        "\U0001F1E8\U0001F1F3": 1493249955400257725,  # Chinese Flag
        "\U0001F1EA\U0001F1FA": 1493249813427388416,  # European Flag
        "\U0001F1FF\U0001F1E6": 1493249914346406030,  # South African Flag
        "\U0001F1FA\U0001F1F8": 1493249872898425034 # United States Flag
    }

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        load_dotenv(override=True)
        r_roles_msg_id = int(os.getenv("REACTION_ROLES_MESSAGE_ID"))

        if payload.message_id != r_roles_msg_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        rid = self.roles[payload.emoji.name]
        role = guild.get_role(rid)

        await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        load_dotenv(override=True)
        r_roles_msg_id = int(os.getenv("REACTION_ROLES_MESSAGE_ID"))

        if payload.message_id != r_roles_msg_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        rid = self.roles[payload.emoji.name]
        role = guild.get_role(rid)

        await user.remove_roles(role)

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
