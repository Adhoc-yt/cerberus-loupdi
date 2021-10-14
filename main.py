import random
import discord
import logging
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
ignored_roles = {"Loup", "Adminitrateur", "Modérateur", "Intervenant", "Streamer"}

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
    "ALA": "Åland Islands",
    "ALB": "Albania",
    "AND": "Andorra",
    "ANT": "Netherlands Antilles",
    "ARE": "United Arab Emirates",
    "ARG": "Argentina",
    "ARM": "Armenia",
    "ASM": "American Samoa",
    "ATA": "Antarctica",
    "ATF": "French Southern Territories",
    "ATG": "Antigua and Barbuda",
    "AUS": "Australia",
    "AUT": "Austria",
    "AZE": "Azerbaijan",
    "BDI": "Burundi",
    "BEL": "Belgium",
    "BEN": "Benin",
    "BFA": "Burkina Faso",
    "BGD": "Bangladesh",
    "BGR": "Bulgaria",
    "BHR": "Bahrain",
    "BHS": "Bahamas",
    "BIH": "Bosnia and Herzegovina",
    "BLM": "Saint Barthélemy",
    "BLR": "Belarus",
    "BLZ": "Belize",
    "BMU": "Bermuda",
    "BOL": "Bolivia",
    "BRA": "Brazil",
    "BRB": "Barbados",
    "BRN": "Brunei Darussalam",
    "BTN": "Bhutan",
    "BVT": "Bouvet Island",
    "BWA": "Botswana",
    "CAF": "Central African Republic",
    "CAN": "Canada",
    "CCK": "Cocos (Keeling) Islands",
    "CHE": "Switzerland",
    "CHL": "Chile",
    "CHN": "China",
    "CIV": "Côte d'Ivoire",
    "CMR": "Cameroon",
    "COD": "Congo, RDC",
    "COG": "Congo",
    "COK": "Cook Islands",
    "COL": "Colombia",
    "COM": "Comoros",
    "CPV": "Cape Verde",
    "CRI": "Costa Rica",
    "CUB": "Cuba",
    "CXR": "Christmas Island",
    "CYM": "Cayman Islands",
    "CYP": "Cyprus",
    "CZE": "Czech Republic",
    "DEU": "Germany",
    "DJI": "Djibouti",
    "DMA": "Dominica",
    "DNK": "Denmark",
    "DOM": "Dominican Republic",
    "DZA": "Algeria",
    "ECU": "Ecuador",
    "EGY": "Egypt",
    "ERI": "Eritrea",
    "ESH": "Western Sahara",
    "ESP": "Spain",
    "EST": "Estonia",
    "ETH": "Ethiopia",
    "FIN": "Finland",
    "FJI": "Fiji",
    "FLK": "Falkland Islands (Malvinas)",
    "FRO": "Faroe Islands",
    "FSM": "Micronesia, Federated States of",
    "GAB": "Gabon",
    "GBR": "United Kingdom",
    "GEO": "Georgia",
    "GGY": "Guernsey",
    "GHA": "Ghana",
    "GIB": "Gibraltar",
    "GIN": "Guinea",
    "GLP": "Guadeloupe",
    "GMB": "Gambia",
    "GNB": "Guinea-Bissau",
    "GNQ": "Equatorial Guinea",
    "GRC": "Greece",
    "GRD": "Grenada",
    "GRL": "Greenland",
    "GTM": "Guatemala",
    "GUF": "French Guiana",
    "GUM": "Guam",
    "GUY": "Guyana",
    "HKG": "Hong Kong",
    "HMD": "Heard Island and McDonald Islands",
    "HND": "Honduras",
    "HRV": "Croatia",
    "HTI": "Haiti",
    "HUN": "Hungary",
    "IDN": "Indonesia",
    "IMN": "Isle of Man",
    "IND": "India",
    "IOT": "British Indian Ocean Territory",
    "IRL": "Ireland",
    "IRN": "Iran",
    "IRQ": "Iraq",
    "ISL": "Iceland",
    "ISR": "Israel",
    "ITA": "Italy",
    "JAM": "Jamaica",
    "JEY": "Jersey",
    "JOR": "Jordan",
    "JPN": "Japan",
    "KAZ": "Kazakhstan",
    "KEN": "Kenya",
    "KGZ": "Kyrgyzstan",
    "KHM": "Cambodia",
    "KIR": "Kiribati",
    "KNA": "Saint Kitts Nevis",
    "KOR": "Korea, Republic of",
    "KWT": "Kuwait",
    "LAO": "Lao People's Democratic Republic",
    "LBN": "Lebanon",
    "LBR": "Liberia",
    "LBY": "Libyan Arab Jamahiriya",
    "LCA": "Saint Lucia",
    "LIE": "Liechtenstein",
    "LKA": "Sri Lanka",
    "LSO": "Lesotho",
    "LTU": "Lithuania",
    "LUX": "Luxembourg",
    "LVA": "Latvia",
    "MAC": "Macao",
    "MAF": "Saint Martin",
    "MAR": "Morocco",
    "MCO": "Monaco",
    "MDA": "Moldova, Republic of",
    "MDG": "Madagascar",
    "MDV": "Maldives",
    "MEX": "Mexico",
    "MHL": "Marshall Islands",
    "MKD": "Macedonia",
    "MLI": "Mali",
    "MLT": "Malta",
    "MMR": "Myanmar",
    "MNE": "Montenegro",
    "MNG": "Mongolia",
    "MNP": "Northern Mariana Islands",
    "MOZ": "Mozambique",
    "MRT": "Mauritania",
    "MSR": "Montserrat",
    "MTQ": "Martinique",
    "MUS": "Mauritius",
    "MWI": "Malawi",
    "MYS": "Malaysia",
    "MYT": "Mayotte",
    "NAM": "Namibia",
    "NCL": "New Caledonia",
    "NER": "Niger",
    "NFK": "Norfolk Island",
    "NGA": "Nigeria",
    "NIC": "Nicaragua",
    "NIU": "Niue",
    "NLD": "Netherlands",
    "NOR": "Norway",
    "NPL": "Nepal",
    "NRU": "Nauru",
    "NZL": "New Zealand",
    "OMN": "Oman",
    "PAK": "Pakistan",
    "PAN": "Panama",
    "PCN": "Pitcairn",
    "PER": "Peru",
    "PHL": "Philippines",
    "PLW": "Palau",
    "PNG": "Papua New Guinea",
    "POL": "Poland",
    "PRI": "Puerto Rico",
    "PRK": "Korea, Democratic People's Republic of",
    "PRT": "Portugal",
    "PRY": "Paraguay",
    "PSE": "Palestinian Territory, Occupied",
    "PYF": "French Polynesia",
    "QAT": "Qatar",
    "REU": "Réunion",
    "ROU": "Romania",
    "RUS": "Russian Federation",
    "RWA": "Rwanda",
    "SAU": "Saudi Arabia",
    "SDN": "Sudan",
    "SEN": "Senegal",
    "SGP": "Singapore",
    "SGS": "South Georgia and the South Sandwich Islands",
    "SHN": "Saint Helena, Ascension and Tristan da Cunha",
    "SJM": "Svalbard and Jan Mayen",
    "SLB": "Solomon Islands",
    "SLE": "Sierra Leone",
    "SLV": "El Salvador",
    "SMR": "San Marino",
    "SOM": "Somalia",
    "SPM": "Saint Pierre and Miquelon",
    "SRB": "Serbia",
    "STP": "Sao Tome and Principe",
    "SUR": "Suriname",
    "SVK": "Slovakia",
    "SVN": "Slovenia",
    "SWE": "Sweden",
    "SWZ": "Swaziland",
    "SYC": "Seychelles",
    "SYR": "Syrian Arab Republic",
    "TCA": "Turks and Caicos Islands",
    "TCD": "Chad",
    "TGO": "Togo",
    "THA": "Thailand",
    "TJK": "Tajikistan",
    "TKL": "Tokelau",
    "TKM": "Turkmenistan",
    "TLS": "Timor-Leste",
    "TON": "Tonga",
    "TTO": "Trinidad and Tobago",
    "TUN": "Tunisia",
    "TUR": "Turkey",
    "TUV": "Tuvalu",
    "TWN": "Taiwan, Province of China",
    "TZA": "Tanzania, United Republic of",
    "UGA": "Uganda",
    "UKR": "Ukraine",
    "UMI": "United States Minor Outlying Islands",
    "URY": "Uruguay",
    "USA": "United States",
    "UZB": "Uzbekistan",
    "VAT": "Vatican",
    "VCT": "Saint Vincent and the Grenadines",
    "VEN": "Venezuela",
    "VGB": "Virgin Islands, British",
    "VIR": "Virgin Islands, U.S.",
    "VNM": "Viet Nam",
    "VUT": "Vanuatu",
    "WLF": "Wallis and Futuna",
    "WSM": "Samoa",
    "YEM": "Yemen",
    "ZAF": "South Africa",
    "ZMB": "Zambia",
    "ZWE": "Zimbabwe"
}
region_roles = set(dict_department_region.values())
region_roles.add(default_role)
region_roles.add(expat_role_name)
country_roles = set(dict_countries_alphacodes.values())


def role_exists(rolename, server: discord.Guild):
    print("Checking if role '{}' exists".format(rolename))
    return discord.utils.get(server.roles, name=rolename)


def has_valid_nick_and_roles(member: discord.Member):
    """
    Retourne si un pseudo est conforme au format demandé,
    ET si les bons rôles sont associés au membre
    """
    # If no nickname, using name
    nickname = member.display_name
    code = nickname.split()[0]
    return code in dict_department_region or code in dict_countries_alphacodes


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
    await member.add_roles(discord.utils.get(member.guild.roles, name=role_country))
    await member.add_roles(discord.utils.get(member.guild.roles, name=expat_role_name))


async def check_roles(member: discord.Member):
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
        else:
            await remove_any_previous_role(member)
            dept_role = get(member.guild.roles, name=dict_department_region.get(code))
            await member.add_roles(dept_role)
            print("Adding department role '{}' to member '{}'".format(dept_role, member))

    elif code in dict_countries_alphacodes:
        print("Checking country code {}".format(code))
        role_country = dict_countries_alphacodes.get(code)
        if role_exists(role_country, member.guild) \
                and discord.utils.get(server_roles, name=expat_role_name) in member.roles \
                and discord.utils.get(server_roles, name=role_country) in member.roles:
            print("Country role {} exists, and is properly assigned "
                  "to {} with expat role".format(role_country, member))
        else:
            print("Checking -> assign role {}".format(role_country))
            await assign_country_role(member, role_country)


async def remove_any_previous_role(member: discord.Member):
    """
    Supprime tout précédent rôle de région au membre s'il en a un
    """
    for role in member.roles:
        if role.name in region_roles or role.name in country_roles:
            print("- Removing role '{}' from member '{}'".format(role, member))
            await member.remove_roles(role)


@bot.event
async def on_ready():
    logging.info(f"Bot online - {bot.user}")


@bot.event
async def on_member_join(member: discord.Member):
    await member.send(f":wave: Bienvenue sur le serveur ! "
                      "Si vous n'avez pas déjà un code pays ou un numéro de département dans votre pseudo, "
                      "__**dans le salon principal**__, veuillez entrer votre **numéro de département** Français, "
                      "ou le code **CIO/Alpha-3** de votre pays si vous n'êtes pas en France.")
    await member.add_roles(discord.utils.get(member.guild.roles, name=default_role))


@bot.command()
@commands.has_role('Admin')
async def setup(ctx):
    """
    c!setup - Vérifie et installe les rôles nécessaires au bon fonctionnement du bot.
    Cette commande ne peut être utilisée que par les 'Admin' (role Discord).
    """
    await ctx.send(f":arrow_forward: Début de vérification des rôles")
    for role in region_roles:
        if role_exists(role, ctx.guild):
            await ctx.send(f":blue_circle: Le rôle **{role}** existe déjà")
        else:
            await ctx.guild.create_role(name=role, colour=discord.Colour(random.randint(0, 0xFFFFFF)))
            await ctx.send(f":green_circle: Le rôle **{role}** a été créé")
    await ctx.send(f":white_check_mark: Fin de vérification des rôles")


@bot.event
async def on_message(message):
    """
    A chaque message posté, une vérification s'impose
    """
    member = message.author
    print("### '{}': '{}'".format(member, message.content))
    # Process commands
    await bot.process_commands(message)

    # Ignore if bot
    if member.bot:
        print("{} is a bot, ignoring".format(member))
        return

    # Ignore if member has a bypass role
    try:
        for role in member.roles:
            print("- verifying if '{}' is a bypass role...".format(role))
            if role.name in ignored_roles:
                print("Bypass role found : '{}'. Skipping verification.".format(role))
                return
    except AttributeError:
        print("Message was sent as a DM.")
        await message.channel.send("_(Psst, je ne réponds pas aux MP, rendez-vous sur le serveur)_")
        return

    # If nickname is invalid or if roles are not correctly assigned - strip from roles and parse message
    if not has_valid_nick_and_roles(member):
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
            await member.remove_roles(discord.utils.get(member.guild.roles, name=default_role))

        # Finally, prompt again and harass
        else:
            await message.author.send("{} - pseudo invalide, Veuillez entrer votre **numéro de département** Français, "
                                      "ou le code **CIO/Alpha-3** de votre pays "
                                      "si vous n'êtes pas en France.".format(member.mention))
    else:
        await check_roles(member)


if __name__ == '__main__':
    discord_key = open("key.txt", "r").read()
    bot.run(discord_key)
