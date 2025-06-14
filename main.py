import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# ── Chargement des variables d’environnement ──────────────────────────────────
load_dotenv()
token = os.getenv("TOKEN_BOT_DISCORD")

# ── Flask / keep-alive (utile sur Replit, Render, etc.) ───────────────────────
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    Thread(target=run).start()

keep_alive()

# ── Discord setup ─────────────────────────────────────────────────────────────
intents = discord.Intents.all()
intents.message_content = True  # indispensable pour lire les messages
bot = commands.Bot(command_prefix="!", intents=intents)

# ── CONFIGURATION À AJUSTER (IDs de rôles / salons) ───────────────────────────
CATEGORY_ID_ALERT      = 1380612379192328232
CHANNEL_ALERT_GENERAL  = 1382041443668852787
ROLE_MILITAIRE_ID      = 1380612378072191120

ROLES_OFFICIERS_GEN_IDs = [
    1380612378231832712, 1380612378231832711, 1380612378231832709,
    1380612378231832708, 1380612378231832707, 1380612378101547080,
    1380612378101547084
]

# ── Hiérarchie (commande !staff) ──────────────────────────────────────────────
STAFF_ROLES = [
    {"name":"▬▬▬┇Officier suprême┇▬▬▬","id":None,"color":None},
    {"name":"『👑』Maréchal de la Fédération Ruzbèkes","id":1380612378231832712,"color":0xff0000},
    {"name":"『👑』Général d'armée","id":1380612378231832711,"color":0xff0000},
    {"name":"▬▬▬┇Officier Généraux┇▬▬▬","id":None,"color":None},
    {"name":"『🏅』Colonel-Général","id":1380612378231832709,"color":0xfffff0},
    {"name":"『🏅』Lieutenant Général","id":1380612378231832708,"color":0xfffff0},
    {"name":"『🏅』Major Général","id":1380612378231832707,"color":0xfffff0},
    {"name":"▬▬▬┇Officiers Supérieurs┇▬▬▬","id":None,"color":None},
    {"name":"『🌟』Colonel","id":1380612378181238933,"color":0x800000},
    {"name":"『🌟』Lieutenant-Colonel","id":1380612378181238932,"color":0x800000},
    {"name":"『🌟』Major","id":1380612378181238931,"color":0x800000},
    {"name":"▬▬▬┇Officiers subalternes┇▬▬▬","id":None,"color":None},
    {"name":"『🛡️』Capitaine","id":1380612378181238929,"color":0x000080},
    {"name":"『🛡️』Lieutenant Sénior","id":1380612378181238928,"color":0x000080},
    {"name":"『🛡️』Lieutenant","id":1380612378181238927,"color":0x000080},
    {"name":"『🛡️』Lieutenant Junior","id":1380612378181238926,"color":0x000080},
    {"name":"▬▬▬┇officier en formation┇▬▬▬","id":None,"color":None},
    {"name":"『⚔️』Aspirant principal","id":1380612378156077166,"color":0x0f0a0a},
    {"name":"『⚔️』Aspirant","id":1380612378156077165,"color":0x0f0a0a},
    {"name":"▬▬▬┇Sous-officiers ┇▬▬▬","id":None,"color":None},
    {"name":"『⚔️』Sergent Major","id":1380612378156077163,"color":0x0f0a0a},
    {"name":"『⚔️』Sergent Sénior","id":1380612378156077162,"color":0x0f0a0a},
    {"name":"『⚔️』Sergent","id":1380612378156077161,"color":0x0f0a0a},
    {"name":"『⚔️』Sergent Junior","id":1380612378156077160,"color":0x0f0a0a},
    {"name":"▬▬▬┇Hommes du rang┇▬▬▬","id":None,"color":None},
    {"name":"『🪖』Caporal","id":1380612378156077158,"color":0x556b2f},
    {"name":"『🪖』Soldat","id":1380612378156077157,"color":0x556b2f},
]

# ── Tableau des grades (commande !pm) ─────────────────────────────────────────
GRADES = {
    "commandement": {
        "commissaire":  "<@762007395202891808>",  # Remplace les IDs
        "commandantPM": "En recherche",
    },
    "gestion": {
        "admin":         "En recherche",
        "securite":      "En recherche",
        "reglementation":"En recherche",
    },
    "application": {
        "sergent":   "En recherche",
        "agents": [
            "En recherche",
        ],
        "stagiaires": [
            "En recherche",
        ],
    },
}

# ─────────────────────── EVENTS ──────────────────────────────────────────────
@bot.event
async def on_ready():
    print(f"✅ Le bot est connecté en tant que {bot.user}")
    # Enregistre les commandes slash pour un serveur spécifique (GUILD_ID)
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)
    print("Commandes slash synchronisées.")

# ─────────────────────── hiérarchie PM ──────────────────────────────────────────────
@bot.command(name="hiérarchiepm")
async def hierarchie_pm(ctx):
    embed = discord.Embed(
        title="🏛️Hiérarchie de la Police Militaire",
        description="Voici la structure hiérarchique actuelle de la Police Militaire:",
        color=0x0055ff
    )

    embed.add_field(
        name="🔺Corps de Commandement et de Directions",
        value=(
            "👮Commissaire Général d'Unité\n"
            "🎖️Colonel de la Police Militaire"
        ),
        inline=False
    )

    embed.add_field(
        name="📂Corps de Gestion Administrative, de Sécurisation et de Réglementation",
        value=(
            "📁Commandant de la Gestion Administrative\n"
            "🛡️Lieutenant de la Sécurisation\n"
            "📏Lieutenant de la Réglementation"
        ),
        inline=False
    )

    embed.add_field(
        name="🛠️Corps d'Encadrement et d'Application",
        value=(
            "🎖️Sergent Militaire\n"
            "👮Gardien Militaire\n"
            "👨‍🎓Policier d'Apprentissage"
        ),
        inline=False
    )

    embed.set_footer(text="Structure hiérarchique officielle de la PM")
    await ctx.send(embed=embed)

# ─────────────────────── COMMANDES ───────────────────────────────────────────

# Ping — simple test de vie
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong ! Je suis bien en ligne.")

# Staff — hiérarchie militaire détaillée
@bot.command()
async def staff(ctx):
    guild = ctx.guild
    embed = discord.Embed(
        title="📋 Liste des Membres de la hiérarchie",
        description=(
            "Voici les grades et membres qui encadrent et assurent le bon "
            "fonctionnement de l'armée."
        ),
        color=0x2f3136
    )
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

    top_color = None
    for role_info in STAFF_ROLES:
        # Séparateur visuel
        if role_info["id"] is None:
            embed.add_field(name=f"**{role_info['name']}**", value="‎", inline=False)
            continue

        role = guild.get_role(role_info["id"])
        if role and role.members:
            mentions = [member.mention for member in role.members]
            if not top_color:
                top_color = role_info["color"]
            embed.add_field(
                name=f"{role_info['name']} ・ {len(mentions)} membre(s)",
                value="\n".join(mentions),
                inline=False
            )
    if top_color:
        embed.color = top_color

    embed.set_footer(
        text="Affiché par le bot",
        icon_url=ctx.author.avatar.url if ctx.author.avatar else None
    )
    await ctx.send(embed=embed)

# PM — organisation militaire (commissaire, commandant PM, etc.)
@bot.command(name="pm")
async def pm(ctx):
    embed = discord.Embed(
        title="📋 Organisation Militaire",
        description="Voici la structure actuelle des effectifs :",
        color=0x1f8b4c
    )
    embed.add_field(
        name="🔺Corp de Commandement et de Directions",
        value=(
            f"👮  Commissaire Général d'Unité : {GRADES['commandement']['commissaire']}\n"
            f"🎖️ Colonel de la Police Militaire : {GRADES['commandement']['commandantPM']}"
        ),
        inline=False
    )
    embed.add_field(
        name="📂Corp de Gestions Administrative de Sécurisations et de la Règlementations",
        value=(
            f"📁Commandant de la Gestions Administrative d'Unité  : {GRADES['gestion']['admin']}\n"
            f"🛡️Lieutenant de Gestions de la Sécurisations : {GRADES['gestion']['securite']}\n"
            f"📏Lieutenant de Gestions de la Règlementations : {GRADES['gestion']['reglementation']}"
        ),
        inline=False
    )
    embed.add_field(
        name="🛠️Corp de d'Encadrement et D'Application",
        value=(
            f"🎖️Sergent Militaire   : {GRADES['application']['sergent']}\n"
            f"👮Gardien Militaire : {', '.join(GRADES['application']['agents'])}\n"
            f"👨‍🎓Policier d'Apprentissage : {', '.join(GRADES['application']['stagiaires'])}"
        ),
        inline=False
    )
    await ctx.send(embed=embed)

    # 🔔 Mention du rôle Police Militaire (remplace ROLE_ID par le vrai ID)
    role_pm_id = 1380612378101547080  # <--- Mets ici l'ID réel du rôle
    await ctx.send(f"<@&{role_pm_id}> veuillez prendre connaissance de cette Hiérarchie.")

    embed.set_footer(text="Dernière mise à jour automatique")
    embed.timestamp = ctx.message.created_at
    await ctx.send(embed=embed)

# Alerte rouge — création du salon dédié
alerte_rouge_message_cache = {}

@bot.command()
@commands.has_any_role(*ROLES_OFFICIERS_GEN_IDs)
async def alerte_rouge(ctx):
    guild = ctx.guild
    category = guild.get_channel(CATEGORY_ID_ALERT)
    if not category:
        await ctx.send("❌ Catégorie introuvable.")
        return

    existing_channel = discord.utils.get(category.text_channels, name="alerte-rouge")
    if existing_channel:
        await ctx.send("⚠️ Le salon `alerte-rouge` existe déjà.")
        return

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        guild.me:           discord.PermissionOverwrite(view_channel=True, send_messages=True)
    }
    for rid in ROLES_OFFICIERS_GEN_IDs:
        role = guild.get_role(rid)
        if role:
            overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

    channel = await guild.create_text_channel(
        "alerte-rouge",
        category=category,
        overwrites=overwrites,
        position=0
    )

    mentions = " ".join(
        guild.get_role(rid).mention for rid in ROLES_OFFICIERS_GEN_IDs if guild.get_role(rid)
    )
    msg = await channel.send(
        f"""{mentions}
🚨 **Alerte rouge déclenchée par {ctx.author.mention}**

Ce salon a été créé afin d’organiser la réponse face à une menace critique.
Merci de rester concentré sur la situation en cours (décisions, informations, directives).

*Maréchal* : quand vous serez prêt, tapez `!alerte_rouge_message` dans <#{CHANNEL_ALERT_GENERAL}> pour envoyer l’alerte officielle à tous les militaires."""
    )
    alerte_rouge_message_cache[channel.id] = msg.id
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

@bot.command()
@commands.has_any_role(*ROLES_OFFICIERS_GEN_IDs)
async def alerte_rouge_message(ctx):
    channel = discord.utils.get(ctx.guild.text_channels, name="alerte-rouge")
    if not channel:
        await ctx.send("⚠️ Le salon `alerte-rouge` n’existe pas.")
        return

    role = ctx.guild.get_role(ROLE_MILITAIRE_ID)
    embed = discord.Embed(
        title="🔴 ALERTE ROUGE - PROCÉDURES MILITAIRES",
        description=(
            "**État d'urgence militaire activé.**\n\n"
            "La **Police Militaire** est maintenant autorisée à :\n"
            "• Porter leur **arme de service**.\n"
            "• Porter leur **tenue de combat**.\n"
            "• Contrôler **tout membre** sans justification.\n"
            "• Considérer comme **suspect** toute personne refusant un contrôle.\n\n"
            "Merci de **coopérer immédiatement**."
        ),
        color=0xff0000
    )
    embed.set_footer(text="Ordre militaire — Fédération Ruzbèkes")
    await channel.send(content=role.mention if role else "", embed=embed)
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass


# ———!cérémonie ——————————————————————
    # 🟪 Le message modifiable ici
TOKEN = 'TOKEN_BOT_DISCORD'

# Remplace par l'ID de ton serveur
GUILD_ID = 1380612378072191116

# Remplace par l'ID du rôle à mentionner
ID_DU_ROLE_MILITAIRE = 1380612378072191120

# Message de la cérémonie
CEREMONIE_TEMPLATE = """
Message de L'État‑Major FAFR : Annonce de la Cérémonie

Messieurs, Bonjour. Je vous annonce en ce jour l'Annonce de la Cérémonie du {date} à {heure} \
accompagnée de la tenue avec le numéro de Série {tenue}, afin de pouvoir remercier et récompenser \
tous les soldats ayant donné leur vie ou bien accompli des exploits et méritant une augmentation hiérarchique.

C'est pour cela que l'État‑Major vous attendra avec impatience lors de cette cérémonie.

Bien cordialement,  
L'État‑Major FAFR.
"""

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')
    # Enregistre les commandes slash pour un serveur spécifique
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)
    print("Commandes slash synchronisées.")

@bot.tree.command(name="cérémonie", description="Annonce une cérémonie militaire")
async def ceremonie(interaction: discord.Interaction, date: str, heure: str, tenue: str):
    try:
        texte = CEREMONIE_TEMPLATE.format(date=date, heure=heure, tenue=tenue)
        embed = discord.Embed(
            title="🎊 Annonce de la Cérémonie 🎊",
            description=texte,
            color=discord.Color.purple()
        )
        embed.set_footer(text="Modifiable dans main.py")

        # Mentionne le rôle
        role = interaction.guild.get_role(ID_DU_ROLE_MILITAIRE)
        if role:
            await interaction.response.send_message(content=f"{role.mention}", embed=embed)
        else:
            await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"❌ Erreur : {e}")

@bot.command(name="cérémonie")
async def ceremonie_prefix(ctx, date: str, heure: str, tenue: str):
    try:
        texte = CEREMONIE_TEMPLATE.format(date=date, heure=heure, tenue=tenue)
        embed = discord.Embed(
            title="🎊 Annonce de la Cérémonie 🎊",
            description=texte,
            color=discord.Color.purple()
        )
        embed.set_footer(text="Modifiable dans main.py")

        # Mentionne le rôle
        role = ctx.guild.get_role(ID_DU_ROLE_MILITAIRE)
        if role:
            await ctx.send(content=f"{role.mention}", embed=embed)
        else:
            await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erreur : {e}")

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")




# ── Lancement du bot ─────────────────────────────────────────────────────────
bot.run(token)
