import discord
from discord.ext import commands
import settings

import sys
sys.path.append('./utils/classes')
import dict_functions as df

class set(commands.Cog):

  def __init__(self, bot):
    self.bot = bot;
    print("Setup cog loaded")

  @commands.group(name = "setup", invoke_without_command = True)
  async def setup(self, ctx):
    if ctx.invoked_subcommand is None:
      async with ctx.typing():
        await ctx.send("This command cannot be invoked without subcommand!")
        embed = discord.Embed(title = "Setup command options", 
                              url = "https://TestyBotty.altervista.org",
                              description = "This is a list of all possible subcommands of the 'setup' command",
                              color=0x33FFBD)
        embed.set_author(name = f"{ctx.author} called the $setup command",
                         icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = "https://cdn.discordapp.com/avatars/863755911125925896/65810bae82b10ab9f098c5c8af273f07.webp?size=256")
        embed.add_field(name = "Here are the commands",
                        value="comandi", 
                        inline=False)
        embed.set_footer(text = "Thanks for using TestyBotty! To help: https://github.com/Michele-Vitali/TestyBotty or https://discord.gg/qx8tHHxDgu")
        await ctx.send(embed = embed)
  
  @setup.command(name = "welcome_channel")
  async def welcome_channel(self, ctx, value):
    print(value)
    guild = next((i for i in settings.servers if i['ID'] == ctx.guild.id), None)
    if guild:
      try:
        guild['welcome_channel'] = value
        df.update_dict(guild, 'welcome_channel', value)
        print(settings.servers)
      except:
        print("Eccezione")

def setup(bot):
  bot.add_cog(set(bot))