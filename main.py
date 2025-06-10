import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# Charger les variables d'environnement
load_dotenv()
token = os.getenv('TOKEN_BOT_DISCORD')

# Flask (pour keep_alive sur Replit, Render, etc.)
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"
def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
def keep_alive():
    Thread(target=run).start()

keep_alive()

# Discord setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# === CONFIGURATION À AJUSTER ===
CATEGORY_ID_ALERT = 1380612379192328232
CHANNEL_ALERT_GENERAL = 1382041443668852787
ROLE_MILITAIRE_ID = 1380612378072191120

ROLES_OFFICIERS_GEN_IDs = [
    1380612378231832712,
    1380612378231832711,
    1380612378231832709,
    1380612378231832708,
    1380612378231832707,
    1380612378101547080
]

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
    {"name":"『🪖』Soldat","id":1380612378156077157,"color":0x556b2f}
]

# === Commandes Discord ===

@bot.event
async def on_ready():
    print(f"✅ Le bot est connecté en tant que {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong ! Je suis bien en ligne.")

@bot.command()
async def staff(ctx):
    guild = ctx.guild
    embed = discord.Embed(
        title="📋 Liste des Membres de la hiérarchie",
        description="Voici les grade et membre qui encadrent et assurent le bon fonctionnement de l'armée.",
        color=0x2f3136
    )
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

    top_color = None
    for role_info in STAFF_ROLES:
        if role_info["id"] is None:
            embed.add_field(name=f"**{role_info['name']}**", value="‎", inline=False)
            continue

        role = guild.get_role(role_info["id"])
        if role and role.members:
            mentions = [m.mention for m in role.members]
            if not top_color:
                top_color = role_info["color"]
            embed.add_field(
                name=f"{role_info['name']} ・ {len(mentions)} membre(s)",
                value="\n".join(mentions),
                inline=False
            )
    if top_color:
        embed.color = top_color

    embed.set_footer(text="Affiché par le bot", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    await ctx.send(embed=embed)

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
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
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

    mentions = " ".join(guild.get_role(rid).mention for rid in ROLES_OFFICIERS_GEN_IDs if guild.get_role(rid))
    msg = await channel.send(
        f"{mentions}\n🚨Maréchal quand vous serez prêt tapez `!alerte_rouge_message` dans https://discord.com/channels/1380612378072191116/1382041443668852787 pour envoyer l'alerte officielle à tous les militaires."
    )
    alerte_rouge_message_cache[channel.id] = msg.id
    try:
        await ctx.message.delete()
    except:
        pass

@bot.command()
@commands.has_any_role(*ROLES_OFFICIERS_GEN_IDs)
async def alerte_rouge_message(ctx):
    if ctx.channel.name != "『🔴』alerte-rouge":
        await ctx.send("❌ Cette commande doit être utilisée dans le salon `#alerte-rouge`.", delete_after=5)
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
    embed.set_footer(text="Ordre militaire - Fédération Ruzbèkes")
    await ctx.send(content=role.mention if role else "", embed=embed)
    try:
        await ctx.message.delete()
    except:
        pass

# Lancer le bot
bot.run(token)