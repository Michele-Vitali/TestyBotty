from discord.ext import commands
import settings

import re
import string

separators = string.punctuation + string.digits + string.whitespace
excluded = string.ascii_letters

class ban(commands.Cog):

  def __init__(self, bot):
    self.bot = bot;
    print("Bna cog loaded")

  """@commands.Cog.listener()
  async def on_message(self, message):
    guild = [i for i in settings.servers if (['ID']) == message.guild.id]

    words_list = guild['ban_words_list']

    for w in words_list:
      formatted_word = f"[{separators}]*".join(list(w))
      regex_true = re.compile(fr"{formatted_word}", re.IGNORECASE)
      regex_false = re.compile(fr"([{excluded}]+{w})|({w}[{excluded}]+)")
  
      profane = False
      if regex_true.search(message.content) is not None\
        and regex_false.search(message.content) is not None:
        profane = True
        await message.channel.send("Parola bannata nel messaggio!")
        break  """

def setup(bot):
  bot.add_cog(ban(bot))