import discord
from discord import option
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    try:
        synced = await bot.sync_commands()
        print(f"Commandes synchronisées : {len(synced)}")
    except Exception as e:
        print(f"Erreur de sync : {e}")

@bot.slash_command(name="grade", description="Affiche les grades des soldats")
async def grade(ctx):
    await ctx.respond("🪖 Grades :\n- Soldat\n- Caporal\n- Sergent\n- Lieutenant\n- Capitaine")

bot.run("TOKEN_BOT_DISCORD")
