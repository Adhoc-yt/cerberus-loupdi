import random
import discord
from discord.ext import commands

# Config bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="c!", intents=intents)

role_invalid_nickname = 'Pseudo non valide'
whitelist_prefixes = []


@bot.command()
@commands.has_role('Admin')
async def setup(ctx):
    """
    %setup - Vérifie et installe les rôles nécessaires au bon fonctionnement du bot.
    Cette commande ne peut être utilisée que par les Admins (role Discord).
    """
    if discord.utils.get(ctx.guild.roles, name=role_invalid_nickname):
        await ctx.send(f"Le rôle {role_invalid_nickname} existe déjà")
    else:
        await ctx.guild.create_role(name=role_invalid_nickname, colour=discord.Colour(random.randint(0, 0xFFFFFF)))
        await ctx.send(f"Le rôle {role_invalid_nickname} a été créé")


if __name__ == '__main__':
    discord_key = open("key.txt", "r").read()
    bot.run(discord_key)
