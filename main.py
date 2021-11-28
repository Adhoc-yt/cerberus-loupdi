import random
import discord
import logging
import re
from discord.ext import commands
from discord.utils import get
from datetime import datetime
import pytz

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

dict_department_region = {
    "01": "Auvergne-Rhône-Alpes",
    "02": "Hauts-de-France",
    "03": "Auvergne-Rhône-Alpes",
    "04": "Provence-Alpes-Côte d'Azur",
    "05": "Provence-Alpes-Côte d'Azur",
    "06": "Provence-Alpes-Côte d'Azur",
    "07": "Auvergne-Rhône-Alpes",
    "08": "Grand Est",
    "09": "Occitanie",
    "10": "Grand Est",
    "11": "Occitanie",
    "12": "Occitanie",
    "13": "Provence-Alpes-Côte d'Azur",
    "14": "Normandie",
    "15": "Auvergne-Rhône-Alpes",
    "16": "Nouvelle-Aquitaine",
    "17": "Nouvelle-Aquitaine",
    "18": "Centre-Val de Loire",
    "19": "Nouvelle-Aquitaine",
    "2A": "Corse",
    "2B": "Corse",
    "21": "Bourgogne-Franche-Comté",
    "22": "Bretagne",
    "23": "Nouvelle-Aquitaine",
    "24": "Nouvelle-Aquitaine",
    "25": "Bourgogne-Franche-Comté",
    "26": "Auvergne-Rhône-Alpes",
    "27": "Normandie",
    "28": "Centre-Val de Loire",
    "29": "Bretagne",
    "30": "Occitanie",
    "31": "Occitanie",
    "32": "Occitanie",
    "33": "Nouvelle-Aquitaine",
    "34": "Occitanie",
    "35": "Bretagne",
    "36": "Centre-Val de Loire",
    "37": "Centre-Val de Loire",
    "38": "Auvergne-Rhône-Alpes",
    "39": "Bourgogne-Franche-Comté",
    "40": "Nouvelle-Aquitaine",
    "41": "Centre-Val de Loire",
    "42": "Auvergne-Rhône-Alpes",
    "43": "Auvergne-Rhône-Alpes",
    "44": "Pays de la Loire",
    "45": "Centre-Val de Loire",
    "46": "Occitanie",
    "47": "Nouvelle-Aquitaine",
    "48": "Occitanie",
    "49": "Pays de la Loire",
    "50": "Normandie",
    "51": "Grand Est",
    "52": "Grand Est",
    "53": "Pays de la Loire",
    "54": "Grand Est",
    "55": "Grand Est",
    "56": "Bretagne",
    "57": "Grand Est",
    "58": "Bourgogne-Franche-Comté",
    "59": "Hauts-de-France",
    "60": "Hauts-de-France",
    "61": "Normandie",
    "62": "Hauts-de-France",
    "63": "Auvergne-Rhône-Alpes",
    "64": "Nouvelle-Aquitaine",
    "65": "Occitanie",
    "66": "Occitanie",
    "67": "Grand Est",
    "68": "Grand Est",
    "69": "Auvergne-Rhône-Alpes",
    "70": "Bourgogne-Franche-Comté",
    "71": "Bourgogne-Franche-Comté",
    "72": "Pays de la Loire",
    "73": "Auvergne-Rhône-Alpes",
    "74": "Auvergne-Rhône-Alpes",
    "75": "Île-de-France",
    "76": "Normandie",
    "77": "Île-de-France",
    "78": "Île-de-France",
    "79": "Nouvelle-Aquitaine",
    "80": "Hauts-de-France",
    "81": "Occitanie",
    "82": "Occitanie",
    "83": "Provence-Alpes-Côte d'Azur",
    "84": "Provence-Alpes-Côte d'Azur",
    "85": "Pays de la Loire",
    "86": "Nouvelle-Aquitaine",
    "87": "Nouvelle-Aquitaine",
    "88": "Grand Est",
    "89": "Bourgogne-Franche-Comté",
    "90": "Bourgogne-Franche-Comté",
    "91": "Île-de-France",
    "92": "Île-de-France",
    "93": "Île-de-France",
    "94": "Île-de-France",
    "95": "Île-de-France",
    "971": "Régions d'outre-mer",
    "972": "Régions d'outre-mer",
    "973": "Régions d'outre-mer",
    "974": "Régions d'outre-mer",
    "975": "Régions d'outre-mer",
    "976": "Régions d'outre-mer",
    "977": "Régions d'outre-mer",
    "978": "Régions d'outre-mer",
    "984": "Régions d'outre-mer",
    "986": "Régions d'outre-mer",
    "987": "Régions d'outre-mer",
    "988": "Régions d'outre-mer",
    "989": "Régions d'outre-mer"
}
dict_countries_alphacodes = {
    "ABW": "Aruba",
    "AFG": "Afghanistan",
    "AGO": "Angola",
    "AIA": "Anguilla",
    "ALA": "Åland",
    "ALB": "Albanie",
    "AND": "Andorre",
    "ANT": "Antilles néerlandaises",
    "ARE": "Émirats arabes unis",
    "ARG": "Argentine",
    "ARM": "Arménie",
    "ASM": "Samoa américaines",
    "ATA": "Antarctique",
    "ATF": "Terres australes françaises",
    "ATG": "Antigua-et-Barbuda",
    "AUS": "Australie",
    "AUT": "Autriche",
    "AZE": "Azerbaïdjan",
    "BDI": "Burundi",
    "BEL": "Belgique",
    "BEN": "Bénin",
    "BFA": "Burkina Faso",
    "BGD": "Bangladesh",
    "BGR": "Bulgarie",
    "BHR": "Bahreïn",
    "BHS": "Bahamas",
    "BIH": "Bosnie-Herzégovine",
    "BLM": "Saint-Barthélemy",
    "BLR": "Bélarus",
    "BLZ": "Belize",
    "BMU": "Bermudes",
    "BOL": "Bolivie",
    "BRA": "Brésil",
    "BRB": "Barbade",
    "BRN": "Brunéi Darussalam",
    "BTN": "Bhoutan",
    "BVT": "Bouvet",
    "BWA": "Botswana",
    "CAF": "République centrafricaine",
    "CAN": "Canada",
    "CCK": "Îles Cocos",
    "CHE": "Suisse",
    "CHL": "Chili",
    "CHN": "Chine",
    "CIV": "Côte d'Ivoire",
    "CMR": "Cameroun",
    "COD": "Congo (RDC)",
    "COG": "Congo",
    "COK": "Îles Cook",
    "COL": "Colombie",
    "COM": "Comores",
    "CPV": "Cap-Vert",
    "CRI": "Costa Rica",
    "CUB": "Cuba",
    "CXR": "Île Christmas",
    "CYM": "Îles Caïmans",
    "CYP": "Chypre",
    "CZE": "Tchéquie",
    "DEU": "Allemagne",
    "DJI": "Djibouti",
    "DMA": "Dominique",
    "DNK": "Danemark",
    "DOM": "République dominicaine",
    "DZA": "Algérie",
    "ECU": "Équateur",
    "EGY": "Égypte",
    "ERI": "Érythrée",
    "ESH": "Sahara occidental",
    "ESP": "Espagne",
    "EST": "Estonie",
    "ETH": "Éthiopie",
    "FIN": "Finlande",
    "FJI": "Fidji",
    "FLK": "Îles Malouines",
    "FRO": "Îles Féroé",
    "FSM": "Micronésie",
    "GAB": "Gabon",
    "GBR": "Royaume-Uni",
    "GEO": "Géorgie",
    "GGY": "Guernesey",
    "GHA": "Ghana",
    "GIB": "Gibraltar",
    "GIN": "Guinée",
    "GLP": "Guadeloupe",
    "GMB": "Gambie",
    "GNB": "Guinée-Bissau",
    "GNQ": "Guinée équatoriale",
    "GRC": "Grèce",
    "GRD": "Grenade",
    "GRL": "Groenland",
    "GTM": "Guatemala",
    "GUF": "Guyane française",
    "GUM": "Guam",
    "GUY": "Guyana",
    "HKG": "Hong Kong",
    "HMD": "Îles Heard et McDonald",
    "HND": "Honduras",
    "HRV": "Croatie",
    "HTI": "Haïti",
    "HUN": "Hongrie",
    "IDN": "Indonésie",
    "IMN": "Île de Man",
    "IND": "Indie",
    "IOT": "Territoire britannique de l'océan Indien",
    "IRL": "Irlande",
    "IRN": "Iran",
    "IRQ": "Irak",
    "ISL": "Islande",
    "ISR": "Israël",
    "ITA": "Italie",
    "JAM": "Jamaïque",
    "JEY": "Jersey",
    "JOR": "Jordanie",
    "JPN": "Japon",
    "KAZ": "Kazakhstan",
    "KEN": "Kenya",
    "KGZ": "Kirghizistan",
    "KHM": "Cambodge",
    "KIR": "Kiribati",
    "KNA": "Saint-Kitts-et-Nevis",
    "KOR": "Corée du Sud",
    "KWT": "Koweït",
    "LAO": "Laos",
    "LBN": "Liban",
    "LBR": "Libéria",
    "LBY": "Libye",
    "LCA": "Sainte-Lucie",
    "LIE": "Liechtenstein",
    "LKA": "Sri Lanka",
    "LSO": "Lesotho",
    "LTU": "Lituanie",
    "LUX": "Luxembourg",
    "LVA": "Lettonie",
    "MAC": "Macao",
    "MAF": "Saint-Martin",
    "MAR": "Maroc",
    "MCO": "Monaco",
    "MDA": "Moldova",
    "MDG": "Madagascar",
    "MDV": "Maldives",
    "MEX": "Mexique",
    "MHL": "Îles Marshall",
    "MKD": "Macédoine du Nord",
    "MLI": "Mali",
    "MLT": "Malte",
    "MMR": "Myanmar",
    "MNE": "Monténégro",
    "MNG": "Mongolie",
    "MNP": "Îles Mariannes du Nord",
    "MOZ": "Mozambique",
    "MRT": "Mauritanie",
    "MSR": "Montserrat",
    "MTQ": "Martinique",
    "MUS": "Maurice",
    "MWI": "Malawi",
    "MYS": "Malaisie",
    "MYT": "Mayotte",
    "NAM": "Namibie",
    "NCL": "Nouvelle-Calédonie",
    "NER": "Niger",
    "NFK": "île Norfolk",
    "NGA": "Nigéria",
    "NIC": "Nicaragua",
    "NIU": "Niue",
    "NLD": "Pays-Bas",
    "NOR": "Norvège",
    "NPL": "Népal",
    "NRU": "Nauru",
    "NZL": "Nouvelle-Zélande",
    "OMN": "Oman",
    "PAK": "Pakistan",
    "PAN": "Panama",
    "PCN": "Pitcairn",
    "PER": "Pérou",
    "PHL": "Philippines",
    "PLW": "Palaos",
    "PNG": "Papouasie-Nouvelle-Guinée",
    "POL": "Pologne",
    "PRI": "Porto Rico",
    "PRK": "Corée du Nord",
    "PRT": "Portugal",
    "PRY": "Paraguay",
    "PSE": "Palestine",
    "PYF": "Polynésie française",
    "QAT": "Qatar",
    "REU": "Réunion",
    "ROU": "Roumanie",
    "RUS": "Russie",
    "RWA": "Rwanda",
    "SAU": "Arabie saoudite",
    "SDN": "Soudan",
    "SEN": "Sénégal",
    "SGP": "Singapour",
    "SGS": "Géorgie du Sud-et-les Îles Sandwich du Sud",
    "SHN": "Sainte-Hélène, Ascension et Tristan da Cunha",
    "SJM": "Svalbard et l'Île Jan Mayen",
    "SLB": "Salomon",
    "SLE": "Sierra Leone",
    "SLV": "Salvador",
    "SMR": "Saint-Marin",
    "SOM": "Somalie",
    "SPM": "Saint-Pierre-et-Miquelon",
    "SRB": "Serbie",
    "STP": "Sao Tomé-et-Principe",
    "SUR": "Suriname",
    "SVK": "Slovaquie",
    "SVN": "Slovénie",
    "SWE": "Suède",
    "SWZ": "Eswatini",
    "SYC": "Seychelles",
    "SYR": "Syrie",
    "TCA": "Îles Turks et Caïques",
    "TCD": "Tchad",
    "TGO": "Togo",
    "THA": "Thaïlande",
    "TJK": "Tadjikistan",
    "TKL": "Tokelau",
    "TKM": "Turkménistan",
    "TLS": "Timor-Leste",
    "TON": "Tonga",
    "TTO": "Trinité-et-Tobago",
    "TUN": "Tunisie",
    "TUR": "Turquie",
    "TUV": "Tuvalu",
    "TWN": "Taïwan",
    "TZA": "Tanzanie",
    "UGA": "Ouganda",
    "UKR": "Ukraine",
    "UMI": "Îles mineures éloignées des États-Unis",
    "URY": "Uruguay",
    "USA": "États-Unis",
    "UZB": "Ouzbékistan",
    "VAT": "Vatican",
    "VCT": "Saint-Vincent-et-les Grenadines",
    "VEN": "Venezuela",
    "VGB": "Îles Vierges britanniques",
    "VIR": "Îles Vierges des États-Unis",
    "VNM": "Viet Nam",
    "VUT": "Vanuatu",
    "WLF": "Wallis-et-Futuna",
    "WSM": "Samoa",
    "YEM": "Yémen",
    "ZAF": "Afrique du Sud",
    "ZMB": "Zambie",
    "ZWE": "Zimbabwe",
    "QUE": "Québec",
    "CH": "Suisse"
}
region_roles = set(dict_department_region.values())
region_roles.add(default_role)
region_roles.add(expat_role_name)
country_roles = set(dict_countries_alphacodes.values())


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
            await message.channel.send(embed=embed)
        elif any(substring in message.content.lower() for substring in ["salut", "bonjour", "coucou", "hello"]):
            output = "J'apprécie la politesse, mais vous parlez à un robot. La consigne est claire: numéro de " \
                     "département ou code pays. **RIEN. D'AUTRE.**"
            embed = discord.Embed(title="Erreur", description="➥ {}".format(output))
            await message.channel.send(embed=embed)
        # Finally, prompt again and harass
        else:
            output = "{} - SVP, veuillez entrer votre numéro de département ou code pays à 3 lettres " \
                     "(exemples en Messages Privés), **RIEN D'AUTRE**. ".format(message.author.mention)
            embed = discord.Embed(title="Erreur", description="➥ {}".format(output))
            embed.add_field(name="Attention", value="➥ Tant que vous n'aurez pas répondu, **seule la modération ** "
                                                    "peut vous lire, et vous n'avez pas accès au reste des salons. Si "
                                                    "vous restez trop longtemps sans répondre, vous serez "
                                                    "éjecté.".format(message.author.mention))
            await message.channel.send(embed=embed)

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
    else:
        await check_roles(member)


async def link_actions(message: discord.Message):
    if detect_url(message) and not re.findall('discord', message.content):
        print("Link detected in '{}'".format(message.channel))
        if message.channel.name not in forbidden_links_channels:
            print("Link is posted in whitelisted channel - Skipping")
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
            print("message supprimé")


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
    embed.add_field(name="Ingrédients", value=" ", inline=False)
    embed.add_field(name="- Farine", value="250g", inline=True)
    embed.add_field(name="- Oeuf", value="4", inline=True)
    embed.add_field(name="- Lait", value="1/2 Litre", inline=True)
    embed.add_field(name="- Sucre", value="2 c à s", inline=True)
    embed.add_field(name="- Sel", value="1 pincée", inline=True)
    embed.add_field(name="- Beurre fondu", value="50 g", inline=True)
    embed.add_field(name="___________________________", value=" ", inline=False)
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
    timezones = ['America/Los_Angeles', 'America/Cayenne', 'Europe/Paris', 'Australia/Sydney']
    res = "```"
    for tz in timezones:
        local_datetime = utcmoment.astimezone(pytz.timezone(tz))
        res += local_datetime.strftime("%Y-%m-%d    %H:%M    [{}]\n".format(tz))

    res += "```"
    return res


@bot.command()
async def time(ctx):
    await ctx.send(get_time())


@bot.command()
async def dlive(ctx):
    await ctx.send("https://dlive.tv/Radio-LoupDi")


@bot.command()
async def youtube(ctx):
    await ctx.send("https://www.youtube.com/channel/UCPQx_gNV37pZCOZ1CaHwq2A")


@bot.command()
async def odysee(ctx):
    await ctx.send("https://odysee.com/@RadioLoupDi:9")


@bot.command()
async def telegram(ctx):
    await ctx.send("https://t.me/RadioLoupDi")


@bot.command()
async def tipeee(ctx):
    await ctx.send("https://fr.tipeee.com/loup-divergent")


@bot.command()
async def loupdi(ctx):
    await ctx.send("```DLive``` https://dlive.tv/Radio-LoupDi "
                   "```YouTube``` https://www.youtube.com/channel/UCPQx_gNV37pZCOZ1CaHwq2A "
                   "```Odysee``` https://odysee.com/@RadioLoupDi:9 "
                   "```Telegram``` https://t.me/RadioLoupDi "
                   "```Tipeee``` https://fr.tipeee.com/loup-divergent ")


@bot.command()
async def annonce(ctx, message):
    print("Tentative d'envoi: '{}'".format(message))
    for channel in bot.get_all_channels():
        try:
            await channel.send("{}".format(message))
        except AttributeError:
            pass


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
    embed = discord.Embed(title="Purger le '{}' ? *(Oui / Warn / Non) * ".format(default_role),
                          description="Oui/Warn/Non")
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
        await message.channel.send(get_time())

    if "crepe" in message.content.lower() or \
            "recette" in message.content.lower() or \
            "crêpe" in message.content.lower():
        await message.channel.send(embed=recette_crepe())


if __name__ == '__main__':
    discord_key = open("key.txt", "r").read()
    bot.run(discord_key)
