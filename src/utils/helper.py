import discord
from discord.ext import commands

permitted_roles = ["Engineer"]

def check_perms():
    async def predicate(ctx):
        for role in ctx.author.roles:
            if role.name in permitted_roles:
                return True

        await ctx.send("You don't have enough permissions to run this command.")
        return False
    return commands.check(predicate)

async def build_embed():
    embed = discord.Embed(
        title="Reaction Roles",
        colour=discord.Colour.blue(),
        description="""
            Get your roles here:
            [WIP]
            """
    )
    return embed
