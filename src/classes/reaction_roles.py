import os

from discord.ext import commands
from dotenv import load_dotenv

class ReactionRoles(commands.Cog):
    roles = {
        "\U0001f7e2": 1493220238202769499,
        "\U0001F7E3": 1493220190832562257
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
