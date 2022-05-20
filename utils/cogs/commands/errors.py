from discord.ext import commands
from discord.ext.commands import CommandNotFound

class errors(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, CommandNotFound):
      await ctx.send(f"There's no `{ctx.message.content}` command, type `$help` for help")

def setup(bot):
  bot.add_cog(errors(bot))