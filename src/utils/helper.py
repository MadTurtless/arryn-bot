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
            **Continents**
            \U0001F1FF\U0001F1E6: Africa
            \U0001F1E8\U0001F1F3: Asia
            \U0001F1E6\U0001F1FA: Australia
            \U0001F1EA\U0001F1FA: Europe
            \U0001F1FA\U0001F1F8: North America
            \U0001F1E7\U0001F1F7: South America
            """
    )
    return embed
