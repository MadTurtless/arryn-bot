import discord

from src.classes.reaction_roles import ReactionRoles

class Client(discord.Client):
    def __init__(self, r_roles_msg_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.r_roles = ReactionRoles()
        self.r_roles_msg_id = r_roles_msg_id

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_raw_reaction_add(self, payload):
        if payload.message_id != self.r_roles_msg_id:
            return

        guild = self.get_guild(payload.guild_id)
        user_id = payload.user_id
        role_name = payload.emoji.name

        await self.r_roles.add_role(guild, user_id, role_name)

    async def on_raw_reaction_remove(self, payload):
        if payload.message_id != self.r_roles_msg_id:
            return

        guild = self.get_guild(payload.guild_id)
        user_id = payload.user_id
        role_name = payload.emoji.name

        await self.r_roles.remove_role(guild, user_id, role_name)
