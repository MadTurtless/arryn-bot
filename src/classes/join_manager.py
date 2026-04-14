import discord
from discord.ext import commands


class JoinManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member:
            return

        guild = member.guild
        role = guild.get_role(1490974238864183326)
        await member.add_roles(role)

async def setup(bot):
    await bot.add_cog(JoinManager(bot))