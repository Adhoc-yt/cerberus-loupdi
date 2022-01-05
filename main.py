import asyncio
import logging
import random
import re
from datetime import datetime
from static import dict_department_region
from static import dict_countries_alphacodes

import discord
import pytz
from discord.ext import commands
from discord.utils import get

# Logging
logging.basicConfig()
logging.info("Starting Logging...")

# Config bot
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="c!", intents=intents)

# Custom parameters
default_role = "Tunnel de la Taniere"
expat_role_name = "Expatriés"
admin_role = "Adminitrateur"
ignored_roles = {
    admin_role,
    "Loup",
    "Modérateur",
    "Intervenant",
    "Streamer"
}
forbidden_links_channels = {
    "la-tanière",
    "bienvenue"
}
discord_links_channel = "liens-discord-et-blogs-telegram"
link_only_channels = {
    "partage-de-vidéos",
    "partage-article-de-presse",
    "musique",
    "liens-discord-et-blogs-telegram"
}

region_roles = set(dict_department_region.values())
region_roles.add(default_role)
region_roles.add(expat_role_name)
country_roles = set(dict_countries_alphacodes.values())


async def temp_post(message: discord.Message, embed: discord.Embed):
    msg = await message.channel.send(embed=embed)
    await asyncio.sleep(10)
    await msg.delete()


def role_exists(rolename, server: discord.Guild):
    print("Checking if role '{}' exists".format(rolename))
    return discord.utils.get(server.roles, name=rolename)


def has_valid_nick(member: discord.Member):
    """
    Retourne si un pseudo est conforme au format demandé,
    ET si les bons rôles sont associés au membre
    """
    # If no nickname, using name
    nickname = member.display_name
    code = nickname.split()[0]
    return code in dict_department_region or code in dict_countries_alphacodes


def has_bypass_role(member: discord.Member):
    """
    Supprime tout précédent rôle de région au membre s'il en a un
    """
    for role in member.roles:
        print("- verifying if '{}' is a bypass role...".format(role))
        if role.name in ignored_roles:
            print("Bypass role found : '{}'. Skipping verification.".format(role))
            return True

    return False


def detect_url(message: discord.Message):
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(), ]|%[0-9a-fA-F][0-9a-fA-F])+', message.content)


async def assign_country_role(member: discord.Member, role_country):
    """
    Assignation d'un rôle de pays et du rôle Expat.
    Si le rôle de pays n'existe pas, le crée sur le serveur.
    """
    if not role_exists(role_country, member.guild):
        print(
            "Country role '{}' for member '{}' does not exist on server, creating it".format(role_country, member))
        await member.guild.create_role(name=role_country, colour=discord.Colour(random.randint(0, 0xFFFFFF)))

    print("Adding expat role and country role '{}' to '{}'".format(role_country, member))
    await remove_any_previous_role(member)
    await member.add_roles(discord.utils.get(member.guild.roles, name=role_country))
    await member.add_roles(discord.utils.get(member.guild.roles, name=expat_role_name))
    await member.remove_roles(discord.utils.get(member.guild.roles, name=default_role))


async def check_roles(member: discord.Member):
    """
    Retourne si les roles pour un membre sont corrects ou non
    ET prend les actions nécessaires pour rétablir les rôles
    """
    # Extra safety for bypass
    if has_bypass_role(member):
        return True

    if not has_valid_nick(member):
        print("Chk_roles - Invalid nickname for '{}'".format(member))
        await remove_any_previous_role(member)
        print("Chk_roles - Default role for '{}'".format(member))
        await member.add_roles(get(member.guild.roles, name=default_role))
        return False

    # If no nickname, using name
    nickname = member.display_name
    code = nickname.split()[0]
    print("Checking roles - testing code {}".format(code))
    server_roles = member.guild.roles
    if code in dict_department_region:
        print("Checking department code {}".format(code))
        role_dept = dict_department_region.get(code)
        check_dept_role = discord.utils.get(server_roles, name=role_dept)
        if check_dept_role in member.roles:
            print("Department role '{}' OK for member '{}'".format(check_dept_role, member))
            return True
        else:
            await remove_any_previous_role(member)
            dept_role = get(member.guild.roles, name=dict_department_region.get(code))
            await member.add_roles(dept_role)
            print("Adding department role '{}' to member '{}'".format(dept_role, member))
            return False

    elif code in dict_countries_alphacodes:
        print("Checking country code {}".format(code))
        role_country = dict_countries_alphacodes.get(code)
        if role_exists(role_country, member.guild) \
                and discord.utils.get(server_roles, name=expat_role_name) in member.roles \
                and discord.utils.get(server_roles, name=role_country) in member.roles:
            print("Country role {} exists, and is properly assigned "
                  "to {} with expat role".format(role_country, member))
            return True
        else:
            print("Checking -> assign role {}".format(role_country))
            await assign_country_role(member, role_country)
            return False


async def remove_any_previous_role(member: discord.Member):
    """
    Supprime tout précédent rôle de région au membre s'il en a un
    """
    for role in member.roles:
        if role.name in region_roles or role.name in country_roles:
            print("- Removing role '{}' from member '{}'".format(role, member))
            await member.remove_roles(role)


async def nickname_actions(message: discord.Message):
    """
    A chaque message posté, une vérification s'impose
    """
    member = message.author
    print("### '{}': '{}'".format(member, message.content))

    # Ignore if member has a bypass role
    try:
        if has_bypass_role(member):
            return
    except AttributeError:
        print("Message was sent as a DM.")
        await message.channel.send("_(Psst, je ne réponds pas aux MP, rendez-vous sur le serveur)_")
        return

    # If nickname is invalid or if roles are not correctly assigned - strip from roles and parse message
    if not has_valid_nick(member):
        print("'{}' is not a valid nickname.".format(member.nick))
        await remove_any_previous_role(member)
        await member.add_roles(discord.utils.get(member.guild.roles, name=default_role))
        print("Adding role '{}' to member '{}'".format(default_role, member))

        # Try to detect department number
        if message.content in dict_department_region.keys():
            member = message.author
            role = discord.utils.get(member.guild.roles, name=dict_department_region.get(message.content))
            await member.add_roles(role)
            print("Adding department role '{}' to member '{}'".format(role, member))
            await message.channel.send("Bien compris, merci - Je donne le rôle {}".format(role))
            await member.edit(nick=message.content + ' - ' + member.name)
            await member.remove_roles(discord.utils.get(member.guild.roles, name=default_role))
            print("- Removing default role '{}' from member '{}'".format(default_role, member))

        # Else, try for country code
        elif message.content.upper() in dict_countries_alphacodes.keys():
            country_code = message.content.upper()
            print("Found a matching country code '{}'".format(country_code))
            member = message.author
            role = dict_countries_alphacodes.get(country_code)
            print("Adding country role '{}' and '{}' to member '{}'".format(role, expat_role_name, member))
            await message.channel.send("Salut l'expatrié ! Je donne le rôle {}.".format(role))
            await member.edit(nick=country_code + ' - ' + member.name)
            await assign_country_role(member, role_country=dict_countries_alphacodes.get(country_code))

        # Else, check if zip code
        elif re.match('[0-9]{5}$', message.content):
            dept_guess = message.content[:2]
            output = "Je n'ai pas demandé un code postal, j'ai demandé un numéro de département. Si votre département" \
                     " est '{}' - veuillez taper '{}', merci.".format(dept_guess, dept_guess)
            embed = discord.Embed(title="Erreur", description="➥ {}".format(output))
            await temp_post(message, embed)
        elif any(substring in message.content.lower() for substring in ["salut", "bonjour",
                                                                        "coucou", "hello", "bonsoir"]):
            output = "J'apprécie la politesse, mais vous parlez à un robot. La consigne est claire: numéro de " \
                     "département ou code pays. **RIEN. D'AUTRE.**"
            embed = discord.Embed(title="Erreur", description="➥ {}".format(output))
            await temp_post(message, embed)
        # Finally, prompt again and harass
        else:
            output = "{} - SVP, veuillez entrer votre numéro de département ou code pays à 3 lettres " \
                     "(exemples en Messages Privés), **RIEN D'AUTRE**. ".format(message.author.mention)
            embed = discord.Embed(title="Erreur", description="➥ {}".format(output))
            embed.add_field(name="Attention", value="➥ Tant que vous n'aurez pas répondu, **seule la modération ** "
                                                    "peut vous lire, et vous n'avez pas accès au reste des salons. Si "
                                                    "vous restez trop longtemps sans répondre, vous serez "
                                                    "éjecté.".format(message.author.mention))
            await temp_post(message, embed)

            mp_embed = discord.Embed(title="Salut {} :wave: !".format(message.author.name),
                                     description="Je suis un robot, et j'aide à accueillir les nouveaux.")
            mp_embed.add_field(name="Pourquoi demande-t-on cette info ?",
                               value="➥ Le but du serveur est de mettre en relation les personnes"
                                     ", et vous permet de repérer rapidement les membres de *votre* "
                                     "région.",
                               inline=False)
            mp_embed.add_field(name="Sur le serveur (pas ici)",
                               value="➥ Veuillez taper un message contenant seulement "
                                     "votre **numéro de département** Français",
                               inline=False)
            mp_embed.add_field(name="Si vous n'êtes pas en France",
                               value="➥ Veuillez taper un message contenant seulement votre code pays à 3 "
                                     "lettres, par exemple 'CHE' la Suisse, 'DZA' pour l'Algérie, etc.",
                               inline=False)
            mp_embed.add_field(name="> Exemples de pseudos **invalides**",
                               value="➥ '34Marcel', 'Algerie Abdel', 'BobDu987'")
            mp_embed.add_field(name="> Exemples de pseudos **valides**",
                               value="➥ '34 - Marcel', 'DZA Abdel', '987 TahitiBob'".format())
            await message.author.send(embed=mp_embed)
        await message.delete()
    else:
        await check_roles(member)


async def link_actions(message: discord.Message):
    if message.channel.name == "textuel-staff":
        # skip
        return
    # Pas de pièce jointe ni de lien dans #partage-de-vidéos
    if message.channel.name == "partage-de-vidéos":
        if not detect_url(message):
            print("Message posted in #partage-vidéos but no video or link posted !")
            await message.channel.send("{}, ce salon est réservé au partage de vidéos, pas de discussion ici"
                                       " - message supprimé.".format(message.author.mention))
            await message.delete()

    # Autre chose que des liens dans les salons de partage
    if detect_url(message):
        if any(domain in message.content.lower() for domain in ['discord.gg', 't.me']):
            print("Tgram or Discord server link detected")
            if message.channel.name != discord_links_channel:
                await message.channel.send("{}, merci de poster les liens Discord et Telegram dans le salon approprié,"
                                           " <#{}> - message supprimé.".format(message.author.mention,
                                                                               '778014952757526549'))
                await message.delete()
    # Lien dans un salon pas approprié
    if detect_url(message) and not re.findall('discord.com', message.content):
        print("Link detected in '{}'".format(message.channel))
        if message.channel.name == discord_links_channel:
            print("Link is posted in Discord/Tgram channel only")
            if re.findall('discord.gg', message.content) or re.findall('t.me', message.content):
                print("Discord/Telegram link detected - pass")
                return
            else:
                print("Not a Discord/Telegram Link - block")
                await message.channel.send("{}, tu as posté dans le mauvais salon - ce salon est réservé aux liens "
                                           "Discord et Telegram, message supprimé.".format(message.author.mention))
                await message.delete()
                return
        if message.channel.name not in forbidden_links_channels:
            print("Link is posted in whitelisted channel - Skipping")
            return
        elif has_bypass_role(message.author):
            print("Link has been posted by someone with a bypass role - Skipping")
        else:
            await message.delete()
            await message.channel.send("{}, pas de liens dans ce salon, merci de poster les liens dans la catégorie "
                                       "appropriée - message supprimé.".format(message.author.mention))
            await message.author.send("Pour info, la règle concernant les liens a été établie le 5 novembre 2020, "
                                      "https://discord.com/channels/632963159619141653/774140334006730782"
                                      "/774141383803273269 - et cette règle a du être renforcée le 19 mai 2021, "
                                      "https://discord.com/channels/632963159619141653/774140334006730782"
                                      "/844824472153489458 - Merci de lire le règlement et de jouer le jeu! :wave:")


@bot.event
async def on_ready():
    logging.info(f"Bot online - {bot.user}")


@bot.event
async def on_member_join(member: discord.Member):
    await member.send(f":wave: Bienvenue sur le serveur ! ")
    await member.add_roles(discord.utils.get(member.guild.roles, name=default_role))


@bot.command()
@commands.has_role(admin_role)
async def setup(ctx):
    """
    c!setup - Vérifie et installe les rôles nécessaires au bon fonctionnement du bot.
    Cette commande ne peut être utilisée que par les Admins (role Discord).
    """
    await ctx.send(f":arrow_forward: Début de vérification des rôles...")
    for role in region_roles:
        if role_exists(role, ctx.guild):
            await ctx.send(f":blue_circle: Le rôle **{role}** existe déjà")
        else:
            await ctx.guild.create_role(name=role, colour=discord.Colour(random.randint(0, 0xFFFFFF)))
            await ctx.send(f":green_circle: Le rôle **{role}** a été créé")
    await ctx.send(f":white_check_mark: Fin de vérification des rôles")


def recette_crepe():
    """
    Embed - Recettes aux crepes
    """
    embed = discord.Embed(title="Recette de crêpes - 4 personnes",
                          description="*Difficulté*: Facile / *Préparation*: 10 mn / *Cuisson*: 15 mn / *Temps*: 25 mn",
                          color=0xffc800)
    embed.add_field(name="Ingrédients", value='\u200b', inline=False)
    embed.add_field(name="- Farine", value="250g", inline=True)
    embed.add_field(name="- Oeuf", value="4", inline=True)
    embed.add_field(name="- Lait", value="1/2 Litre", inline=True)
    embed.add_field(name="- Sucre", value="2 c à s", inline=True)
    embed.add_field(name="- Sel", value="1 pincée", inline=True)
    embed.add_field(name="- Beurre fondu", value="50 g", inline=True)
    embed.add_field(name="___________________________", value='\u200b', inline=False)
    embed.add_field(name="1", value="Mettez la farine dans un saladier avec le sel et le sucre.", inline=False)
    embed.add_field(name="2", value="Faites un puits au milieu et versez-y les œufs.", inline=False)
    embed.add_field(name="3",
                    value="Commencez à mélanger doucement. Quand le mélange devient épais, ajoutez le lait froid "
                          "petit à petit.",
                    inline=False)
    embed.add_field(name="4",
                    value="Quand tout le lait est mélangé, la pâte doit être assez fluide. Si elle vous paraît trop "
                          "épaisse, rajoutez un peu de lait. Ajoutez ensuite le beurre fondu refroidi, mélangez bien.",
                    inline=False)
    embed.add_field(name="5",
                    value="Faites cuire les crêpes dans une poêle chaude (par précaution légèrement huilée si votre "
                          "poêle à crêpes n'est pas anti-adhésive). Versez une petite louche de pâte dans la poêle, "
                          "faites un mouvement de rotation pour répartir la pâte sur toute la surface. Posez sur le "
                          "feu et quand le tour de la crêpe se colore en roux clair, il est temps de la retourner.",
                    inline=False)
    embed.add_field(name="6", value="Laissez cuire environ une minute de ce côté et la crêpe est prête.", inline=False)
    return embed


def get_time():
    """
    c!time - Donne l'heure partout (ou presque)
    """
    utcmoment_naive = datetime.utcnow()
    utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)
    timezones = ['Pacific/Tahiti', 'America/Los_Angeles', 'America/Cayenne', 'Europe/Paris', 'Australia/Sydney']

    embed = discord.Embed(title="Heure dans le monde", url="https://24timezones.com/horloge_mondiale.php",
                          description="En ce moment, il est :")
    for tz in timezones:
        local_datetime = utcmoment.astimezone(pytz.timezone(tz))
        embed.add_field(name=tz,
                        value=local_datetime.strftime("%Y-%m-%d    %H:%M    [{}]\n".format(tz)),
                        inline=False)

    return embed


@bot.command()
async def time(ctx):
    await ctx.send(embed=get_time())


@bot.command()
async def dlive(ctx):
    embed = discord.Embed(title="Lien Dlive", url="https://dlive.tv/Radio-LoupDi")
    await ctx.send(embed=embed)


@bot.command()
async def youtube(ctx):
    embed = discord.Embed(title="Lien Youtube", url="https://www.youtube.com/channel/UCPQx_gNV37pZCOZ1CaHwq2A")
    await ctx.send(embed=embed)


@bot.command()
async def odysee(ctx):
    embed = discord.Embed(title="Lien Odysee", url="https://odysee.com/@RadioLoupDi:9")
    await ctx.send(embed=embed)


@bot.command()
async def telegram(ctx):
    embed = discord.Embed(title="Lien Telegram", url="https://t.me/RadioLoupDi")
    await ctx.send(embed=embed)


@bot.command()
async def tipeee(ctx):
    embed = discord.Embed(title="Lien Tipeee", url="https://fr.tipeee.com/loup-divergent")
    await ctx.send(embed=embed)


@bot.command()
async def serveur(ctx):
    embed = discord.Embed(title="Lien Discord", url="https://discord.gg/7sbB6xAJtq")
    await ctx.send(embed=embed)


@bot.command()
async def carte(ctx):
    embed = discord.Embed(title="Lien de la Carte", url="http://u.osmfr.org/m/660805")
    await ctx.send(embed=embed)


@bot.command()
async def loupdi(ctx):
    await dlive(ctx)
    await youtube(ctx)
    await odysee(ctx)
    await telegram(ctx)
    await tipeee(ctx)
    await serveur(ctx)
    await carte(ctx)


@bot.command()
async def annonce(ctx, message):
    print("Tentative d'envoi: '{}'".format(message))
    text_channels = []
    for server in bot.guilds:
        for channel in server.channels:
            if str(channel.type) == 'text':
                text_channels.append(channel)
    # text_channels = bot.get_all_channels()
    for channel in text_channels:
        print("- Trying to send '{}' in #{}".format(message, channel))
        # await channel.send("{}".format(message))


@bot.command()
async def annonce_regions(ctx, message):
    print("Tentative d'envoi pour les régions: '{}'".format(message))
    regions = get(ctx.guild.categories, id=777638347799265330).text_channels
    for region in regions:
        print("- Trying to send '{}' in #{}".format(message, region))
        await region.send(message)


@bot.command()
async def selfname(ctx, nickname):
    embed = discord.Embed(title="Changement de pseudo", description="➥ {}".format(nickname))
    await ctx.guild.get_member(bot.user.id).edit(nick=nickname)
    await ctx.send(embed=embed)


@bot.command()
async def dept(ctx, dept_number):
    if dept_number in dict_department_region.keys():
        await ctx.send("Département {}: {}".format(dept_number, dict_department_region.get(dept_number)))
    else:
        await ctx.send("Département non reconnu. Commande: ```c!dept <numéro_département>```")


@bot.command()
@commands.has_any_role(admin_role, 'Modérateur')
async def scan(ctx):
    """
    c!scan - Vérifie et actualise les rôles de tous les membres d'un serveur.
    Cette commande ne peut être utilisée que par les Admins/Modos (role Discord).
    """
    members_list = ctx.guild.members
    members_scanned_count = 0
    corrected_members_count = 0
    bypass_members_count = 0
    invalid_members_count = 0

    await ctx.send("{} membres trouvés - analyse en cours...".format(len(members_list)))
    for member in members_list:
        if has_bypass_role(member):
            bypass_members_count += 1
        elif not await check_roles(member):
            if has_valid_nick(member):
                corrected_members_count += 1
            else:
                invalid_members_count += 1

        members_scanned_count += 1

    embed = discord.Embed(title="Membres scannés", description="➥ {}".format(members_scanned_count))
    embed.add_field(name="Rôle spécial", value="➥ {}".format(bypass_members_count), inline=True)
    embed.add_field(name="Rôle édité", value="➥ {}".format(corrected_members_count), inline=True)
    embed.add_field(name="Pseudos invalides", value="➥ {}".format(invalid_members_count), inline=True)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_any_role(admin_role, 'Modérateur')
async def scan_member(ctx, member: discord.Member):
    """
    c!scan_member - Vérifie et actualise les rôles d'un membre particulier du serveur.
    Cette commande ne peut être utilisée que par les Admins/Modos (role Discord).
    """
    if await check_roles(member):
        if has_bypass_role(member):
            msg = "Rôle spécial trouvé - ignoré"
        else:
            msg = "Pseudo et rôles validés"
    elif has_valid_nick(member):
        msg = "Rôles corrigés"
    else:
        msg = "Pseudo invalide - Rôle par défaut attribué"

    embed = discord.Embed(title="Vérification de {}".format(member), description="{}".format(msg))
    await ctx.send(embed=embed)
    await ctx.send(":white_check_mark: Fin de vérification pour {}.".format(member))


@bot.command()
@commands.has_any_role(admin_role, 'Modérateur')
async def purge(ctx):
    """
    c!purge - Avertit ou exclut toutes les personnes qui ont le rôle par défaut
    """
    role_purge = discord.utils.get(ctx.guild.roles, name=default_role)
    count_kick = 0
    embed = discord.Embed(title="Purger le '{}' ?".format(default_role),
                          description="Réponses possibles: Oui/Warn/Non")
    await ctx.send(embed=embed)
    msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

    embed = discord.Embed(
        title=":x: Adios pepitos!",
        color=discord.Colour.purple()
    )

    if msg.content.lower() == "oui":
        embed.set_image(url="https://media1.giphy.com/media/l0HlE1P55SaoknGhO/giphy.gif")

        for member in ctx.guild.members:
            if role_purge in member.roles:
                await ctx.guild.kick(member, reason="Pseudo non conforme")
                count_kick += 1
                print("Le membre {} a été expulsé".format(member.name))
        embed.add_field(name="Purge terminée", value="-> {} membre(s) purgés(s)".format(count_kick), inline=False)

    elif msg.content.lower() == "warn":
        await ctx.send(":gun: Avertissement de purge activé.")
        for member in ctx.guild.members:
            if role_purge in member.roles:
                await member.send("{} - dernier avertissement, mise en règle sinon kick.".format(member.mention))
                count_kick += 1
                print("Le membre {} a été averti".format(member.name))
        embed.add_field(name="Avertissement envoyé", value="-> {} membre(s) averti(s)".format(count_kick),
                        inline=False)
    else:
        embed.add_field(name="Commande annulée", value="", inline=False)

    await ctx.send(embed=embed)


@bot.event
async def on_message(message):
    # Process commands
    await bot.process_commands(message)

    # Ignore if bot
    if message.author.bot:
        print("{} is a bot, ignoring".format(message.author))
        return

    await nickname_actions(message)
    await link_actions(message)

    if "quelle heure" in message.content.lower():
        await message.channel.send(embed=get_time())

    if "crepe" in message.content.lower() or \
            "crêpe" in message.content.lower():
        await message.channel.send(embed=recette_crepe())


if __name__ == '__main__':
    discord_key = open("key.txt", "r").read()
    bot.run(discord_key)
