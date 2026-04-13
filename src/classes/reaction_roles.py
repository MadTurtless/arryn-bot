class ReactionRoles:
    roles = {
        "\U0001f7e2": 1493220238202769499,
        "\U0001F7E3": 1493220190832562257
    }

    def __init__(self):
        return

    async def add_role(self, guild, user_id, role_name):
        rid = self.roles[role_name]
        role = guild.get_role(rid)
        user = guild.get_member(user_id)

        if not role or not user:
            return

        await user.add_roles(role)

    async def remove_role(self, guild, user_id, role_name):
        rid = self.roles[role_name]
        role = guild.get_role(rid)
        user = guild.get_member(user_id)

        if not role or not user:
            return

        await user.remove_roles(role)
