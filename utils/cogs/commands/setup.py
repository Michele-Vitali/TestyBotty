import discord
from discord.ext import commands
import settings

import sys
sys.path.append('./utils/classes')
import dict_functions as df
import embed as emb

class set(commands.Cog):

  def __init__(self, bot):
    self.bot = bot;
    print("Setup cog loaded")

  @commands.group(name = "setup", invoke_without_command = True)
  async def setup(self, ctx):
    if ctx.invoked_subcommand is None:

      commands_list = list(self.bot.commands)
      group = None
      
      for c in commands_list:
        if isinstance(c, discord.ext.commands.Group):
          if c.qualified_name == "setup":
            group = c

      group_commands = list(group.commands)
      commands = ""
      for c in group_commands:
        commands += f"- `{c.qualified_name.split(' ', 1)[1]}`, {c.description}\n\n"
      
      async with ctx.typing():
        await ctx.send("This command cannot be invoked without subcommand!")
        embed = emb.build_embed("Setup command options",
                         "https://Discord-Bot.mikyv.repl.co",
                         "This is a list of all possible subcommands of the `setup` command",
                         0x33FFBD,
                         f"{ctx.author} called the $setup command",
                         ctx.author.avatar_url,
                         "https://cdn.discordapp.com/avatars/863755911125925896/65810bae82b10ab9f098c5c8af273f07.webp?size=256",
                         "Here are the commands",
                         commands,
                         False, 
                         "Thanks for using TestyBotty! To help: https://github.com/Michele-Vitali/TestyBotty or https://discord.gg/qx8tHHxDgu",
                         ctx)
        await ctx.send(embed = embed)

  @setup.command(name = "setup_channel", description = "update the setup_channel for this server")
  async def setup_channel(self, ctx, value):
    await self.update_channel(ctx, 'setup_channel', value, "Setup channel")
  
  @setup.command(name = "welcome_channel", description = "update the welcome_channel for this server")
  async def welcome_channel(self, ctx, value):
    await self.update_channel(ctx, "welcome_channel", value, "Welcome channel")

  @setup.command(name = "goodbye_channel", description = "update the goodbye_channel for this server")
  async def goodbye_channel(self, ctx, value):
    await self.update_channel(ctx, "goodbye_channel", value, "Goodbye channel")
  
  async def update_channel(self, ctx, property, value, string):
    guild = next((i for i in settings.servers if i['ID'] == ctx.guild.id), None)
    if guild:
      channels_name = []
      for c in ctx.guild.text_channels:
        channels_name.append(c.name)
      if value in channels_name:
        are_there_copies = channels_name.count(value) > 1
        if not are_there_copies:
          channel_id = discord.utils.get(ctx.guild.channels, name = value).id
          df.update_dict(guild, property, channel_id)
          await ctx.send(f"{string} successfully updated!")
        else:
          await ctx.send("There is more than one channel with that name")
      else:
        await ctx.send("Couldn't find a channel with that name...")

  
  @setup.command(name = "welcome_image", description = "update the welcome_image for this server")
  async def welcome_image(self, ctx):
   await  self.update_image(ctx, 'welcome.png')

  @setup.command(name = "goodbye_image", description = "update the goodbye_image for this server")
  async def goodbye_image(self, ctx):
    await self.update_image(ctx, 'goodbye.png')
  
  async def update_image(self, ctx, path):
    guild = next((i for i in settings.servers if i['ID'] == ctx.guild.id), None)
    if guild:
      try:
        image = ctx.message.attachments[0]
        if image is not None:
          await image.save(f"utils/images/{ctx.guild.id}/{path}")
      except:
        await ctx.send("There's no image attached to this message")

  @setup.command(name = "welcome_image_message", description = "update the welcome_image_message for this server")
  async def welcome_image_message(self, ctx, message):
    await self.update_message(ctx, 'welcome_image_message', message, "Welcome image message")

  @setup.command(name = "goodbye_image_message", description = "update the goodbye_image_message for this server")
  async def goodbye_image_message(self, ctx, message):
    await self.update_message(ctx, 'goodbye_image_message', message, "Goodbye image message")

  @setup.command(name = "welcome_text_message", description = "update the welcome_text_message for this server")
  async def welcome_text_message(self, ctx, message):
    await self.update_message(ctx, 'welcome_text_message', message, 'Welcome text message')

  @setup.command(name = "goodbye_text_message", description = "update the goodbye_text_message for this server")
  async def goodbye_text_message(self, ctx, message):
    await self.update_message(ctx, 'goodbye_text_message', message, 'Goodbye text message')
  
  async def update_message(self, ctx, property, message, string):
    guild = next((i for i in settings.servers if i['ID'] == ctx.guild.id), None)
    if guild:
      df.update_dict(guild, property, message)
      await ctx.send(f"{string} successfully updated!")
    else:
      await ctx.send(f"Error finding the server ID")

  @setup.command(name = "warn_before_ban", description = "update the warns before ban for this server")
  async def warn_before_ban(self, ctx, num):
    guild = next((i for i in settings.servers if i['ID'] == ctx.guild.id), None)
    if guild:
      num = int(num)
      if num < 1:
        num = -1
      df.update_dict(guild, 'warn_before_ban', num)
      await ctx.send("Warns before ban updated successfully!")

def setup(bot):
  bot.add_cog(set(bot))