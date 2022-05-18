import discord
from discord.ext import commands

class help(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    print("Help command loaded")
  
  @commands.command(name = 'help', aliases = ['h'])
  async def help(self, ctx):
    embed = discord.Embed(title = "TestyBotty helper",
                         url = "https://TestyBotty.altervista.org",
                         description = "Having some difficulties? Don't worry \n\n Just type: !help `command_name` to get help about that specific command!",
                         color = 0x33FFBD)
    embed.set_author(name = f"{ctx.author} called the !help command",
                    icon_url = ctx.author.avatar_url)
    embed.set_thumbnail(url = "https://cdn.discordapp.com/avatars/863755911125925896/65810bae82b10ab9f098c5c8af273f07.webp?size=256")

    commands_list = """- `music`, to see all commands for playing music
    
                       - `levels`, to see all options for the leveling system"""
    
    embed.add_field(name = "Commands buddy",
                    value = commands_list,
                   inline = False)
    embed.set_footer(text = "Thanks for using TestyBotty! To help: https://github.com/Michele-Vitali/TestyBotty or https://discord.gg/qx8tHHxDgu")
    
    await ctx.send(embed = embed)

def setup(bot):
  bot.add_cog(help(bot))