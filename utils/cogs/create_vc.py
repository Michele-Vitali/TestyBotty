import discord
from discord.ext import commands
import settings

class create_vc(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    print("VC cog loaded")

  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    guild = next((i for i in settings.servers if i['ID'] == member.guild.id), None)
    join_create_vc = guild['join_to_create_vc']
    vc_administration = guild['vc_admin']
    vc_category = guild['vc_category']
    guild_roles = member.guild.roles
    vc_owner_role = discord.utils.get(member.guild.roles, name = "VC Owner")
    if not vc_owner_role:
      await member.guild.create_role(name = "VC Owner", colour = 0x5AE09D)
      vc_owner_role = discord.utils.get(member.guild.roles, name = "VC Owner")
      
    guild_channels = member.guild.channels
    
    if before.channel == None and after.channel.id == join_create_vc:
      if after.channel.id == join_create_vc:
        name = f"{member.name}'s VC"
        category = discord.utils.get(member.guild.categories, id = vc_category)
        overwrites = {
          member.guild.default_role: discord.PermissionOverwrite(view_channel=False),
          member.guild.default_role: discord.PermissionOverwrite(connect=False),
          vc_owner_role: discord.PermissionOverwrite(view_channel=True)
        }
        
        new_vc = await member.guild.create_voice_channel(name, overwrites = overwrites, category = category)
        await member.move_to(new_vc)
        await member.add_roles(vc_owner_role)
    elif before.channel != None and before.channel.id != join_create_vc:
      voice_state = member.guild.voice_client
      if voice_state:
        if len(voice_state.channel.members) == 1:
          await before.channel.delete()
          await member.remove_roles(vc_owner_role)

      if len(before.channel.members) == 0:
        await before.channel.delete()
        await member.remove_roles(vc_owner_role)
    elif f"{member.name}' VC" in str(guild_channels):
      vc_ad_channel = discord.utils.get(member.guild.channels, id = vc_administration)
      await vc_ad_channel.send(f"{member.mention} there's already a VC with your name, join there")

def setup(bot):
  bot.add_cog(create_vc(bot))