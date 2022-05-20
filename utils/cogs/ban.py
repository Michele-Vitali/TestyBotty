import discord
from discord.ext import commands
import settings

import re
import string

separators = string.punctuation + string.digits + string.whitespace
excluded = string.ascii_letters

class ban(commands.Cog):

  def __init__(self, bot):
    self.bot = bot;
    print("Ban cog loaded")

  @commands.Cog.listener()
  async def on_message(self, message):
    guild = next((i for i in settings.servers if i['ID'] == message.guild.id), None)

    words_list = guild['ban_words_list']

    separators = string.punctuation + string.digits + string.whitespace
    excluded = string.ascii_letters
    
    for w in words_list:
      formatted_word = f"[{separators}]*".join(list(w))
      regex_true = re.compile(fr"{formatted_word}", re.IGNORECASE)
      regex_false = re.compile(fr"([{excluded}]+{w})|({w}[{excluded}]+)", re.IGNORECASE)
  
      profane = False

      if regex_true.search(message.content) is not None and regex_false.search(message.content) is None:
        profane = True
        await message.delete()
        await message.channel.send(f"{message.author.mention} ha scritto una parola bannata nel messaggio!")
        break

    if profane:
      warn_count = guild['warn_before_ban']
      warn_colour = int(255 / warn_count)
      warn_colour_difference = warn_colour
      if warn_count > 0:
        for i in range(warn_count):
          colour = "0x{:X}0000".format(warn_colour)
          warn_colour += warn_colour_difference
          role_name = f"Warn {i+1}"
          if not discord.utils.get(message.guild.roles, name = role_name):
            await message.guild.create_role(name = role_name, colour = int(colour, 0))
        
        warn_number = 0
        for r in message.author.roles:
          if "Warn " in r.name:
            warn_number = int(r.name[5:])
          else:
            warn_number = 0
          if warn_number > warn_count:
            await message.author.ban(reason = "You said too many bad words in your messages")
          else:
            next_warn = discord.utils.get(message.guild.roles, name = f"Warn {warn_number + 1}")
            await message.author.add_roles(next_warn)

def setup(bot):
  bot.add_cog(ban(bot))