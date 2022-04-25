from discord.ext import commands
import settings

class ServerJoinExit(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    print("Server join-exit cog loaded")

  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    #Leggo il file
    servers = settings.servers
    #Creo un nuovo dictionry del server dove sono appena joinato
    obj = {
      "ID": guild.id,
      "name": guild.name,
      "welcome_channel": "",
      "welcome_image": "",
      "welcome_image_message": "",
      "welcome_text_message": "",
      "goodbye_channel": "",
      "goodbye_image": "",
      "goodbye_image_message": "",
      "goodbye_text_message": "",
      "setup-channel": "",
      "ban_words_list": []
    }
    #Aggiungo il nuovo server alla lista dei servers
    servers.append(obj)
    #Salvo nel file la lista dei server aggiornata
    settings.rw.write(servers)
    print(f"I joined {guild.name} server, yay!")

  @commands.Cog.listener()
  async def on_guild_remove(self, guild):
    #Leggo il file
    servers = settings.servers
    #Ottengo la nuova lista di server dove non è presente quello da dove sono uscito
    #Ref: https://www.geeksforgeeks.org/python-removing-dictionary-from-list-of-dictionaries/
    servers = [i for i in servers if not (i['ID']) == guild.id]
    #Salvo nel file la lista dei server aggiornata
    settings.rw.write(servers)
    print(f"I got kicked from {guild.name} server, uff!")

def setup(bot):
  bot.add_cog(ServerJoinExit(bot))