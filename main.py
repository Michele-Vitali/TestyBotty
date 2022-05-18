import discord
from discord.ext import commands
import os

from keep_alive import keep_alive
import settings

intents = discord.Intents.all()
intents.members = True
activity = discord.Game(name="!Help")
status = discord.Status.idle
bot = commands.Bot(command_prefix="$",
                   help_command = None,
                   guild_subscriptions = True,
                   intents = intents, activity = activity, status = status)

bot.remove_command("help")

settings.init()

@bot.event
async def on_ready():
  for filename in os.listdir("./utils/cogs"):
    if filename.endswith(".py"):
      bot.load_extension(f"utils.cogs.{filename[:-3]}")

  for filename in os.listdir('./utils/cogs/commands'):
    if filename.endswith('.py'):
      bot.load_extension(f"utils.cogs.commands.{filename[:-3]}")
  
  print(f"Logged in as {bot.user}")

my_secret = os.environ['TOKEN']

keep_alive()
bot.run(my_secret)