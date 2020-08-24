import os
from discord.utils import get, find

from paramsGetter import getGuildId

async def hasRoles(member, roles):
    if isinstance(roles, str):
        return get(member.roles, name=roles)
    elif isinstance(roles, list):
        containsAll = True
        for role in roles:
            if isinstance(role, str) and not get(member.roles, name=role):
                containsAll = False
                break
        return containsAll
    return False

async def hasAtLeastOneRole(member, roles):
    if isinstance(roles, str):
        return get(member.roles, name=roles)
    elif isinstance(roles, list):
        for role in roles:
            if isinstance(role, str) and get(member.roles, name=role):
                return True
    return False

async def handleRoles(bot, roles, fct):
    guildId = await getGuildId()
    guild = find(lambda g: g.id == guildId, bot.guilds)
    if guild:
        if isinstance(roles, str):
            role = get(guild.roles, name=roles)
            if role:
                await fct(role)
        elif isinstance(roles, list):
            rolesToSend = []
            for it in roles:
                role = get(guild.roles, name=it)
                if role:
                    rolesToSend.append(role)
            await fct(*rolesToSend)

async def addRoles(bot, member, roles):
    await handleRoles(bot, roles, member.add_roles)

async def removeRoles(bot, member, roles):
    await handleRoles(bot, roles, member.remove_roles)

async def createMuteRole(guild: discord.Guild, roleToCopyPermissionsFrom: discord.Role, muteRoleName: str):
    muteRole = get(guild.roles, name=muteRoleName)

    if not muteRole:
        await guild.create_role(name=muteRoleName)
        muteRole = get(guild.roles, name=muteRoleName)

    for channel in guild.text_channels:
        await asyncio.sleep(0)

        mutePermissions = discord.PermissionOverwrite()
        await setMutedPermissions(mutePermissions)

        if roleToCopyPermissionsFrom:
            overwrites = channel.overwrites_for(roleToCopyPermissionsFrom)
            if overwrites.is_empty():
                await channel.set_permissions(muteRole, overwrite=mutePermissions)
            else:
                await setMutedPermissions(overwrites)
                await channel.set_permissions(muteRole, overwrite=overwrites)

    return muteRole

async def deleteMuteRole(guild: discord.Guild, muteRoleName: str):
    muteRole = get(guild.roles, name=muteRoleName)
    if muteRole:
        for channel in guild.text_channels:
            await asyncio.sleep(0)
            await channel.set_permissions(muteRole, overwrite=None)
