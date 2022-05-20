from discord.ext import commands
import settings

import sys
sys.path.append('./utils/classes')
import dict_functions as df
import embed as emb

class ban_words(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(name = "ban_words_list", aliases = ['bwl'])
  async def ban_words_list(self, ctx):
    guild = next((i for i in settings.servers if i['ID'] == ctx.guild.id), None)

    string = ""

    for c in guild['ban_words_list']:
      string += f"- `{c}`\n"

    if not string:
      string = "There are no banned words in this server!"

    async with ctx.typing():
      embed = emb.build_embed(f"Server: {ctx.guild.name}",
                       "https://Discord-Bot.mikyv.repl.co",
                       f"This is the list of banned words for this {ctx.guild.name}'s server",
                       0x33FFBD,
                       f"{ctx.author} called the $setup command",
                       ctx.author.avatar_url,
                       "https://cdn.discordapp.com/avatars/863755911125925896/65810bae82b10ab9f098c5c8af273f07.webp?size=256",
                       "Banned words", 
                       string,
                       False,
                       "Thanks for using TestyBotty! To help: https://github.com/Michele-Vitali/TestyBotty or https://discord.gg/qx8tHHxDgu",
                       ctx)
  
      await ctx.send(embed = embed)
  
  @commands.command(name = "add_ban_word", aliases = ["abw"])
  async def add_ban_word(self, ctx, *words):
    await self.update_ban_words_list(ctx, True, words)

  @commands.command(name = "remove_ban_word", aliases = ['rbw'])
  async def remove_ban_word(self, ctx, *words):
    await self.update_ban_words_list(ctx, False, words)

  async def update_ban_words_list(self, ctx, add, words):
    guild = next((i for i in settings.servers if i['ID'] == ctx.guild.id), None)
    if guild:
      new_list = guild['ban_words_list']
      async with ctx.typing():
        for w in words:
          if add:
            if w not in new_list:
              new_list.append(w)
              await ctx.send(f"`{w}` added to the banned words!")
            else:
              await ctx.send(f"`{w}` is already present in the banned words!")
          else:
            if w in new_list:
              new_list.remove(w)
              await ctx.send(f"`{w}` removed from the banned words!")
            else:
                await ctx.send("There's no such word in the current ban words list, type $ban_words_list to see the list of words")
            
      df.update_dict(guild, 'ban_words_list', new_list)

def setup(bot):
  bot.add_cog(ban_words(bot))