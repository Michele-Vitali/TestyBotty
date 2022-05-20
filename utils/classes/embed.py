import discord

def build_embed(title = "", title_url = "", description = "", color = 0x000000,
               author_name = "", icon_url = "", thumbnail_url = "", 
                field_name = "", value = "", inline = False, footer_text = "", ctx = None):
  embed = discord.Embed(title = title, 
                                url = title_url,
                                description = description,
                                color= color)
  embed.set_author(name = author_name,
                           icon_url = ctx.author.avatar_url)
  embed.set_thumbnail(url = thumbnail_url)
  embed.add_field(name = field_name,
                          value = value, 
                          inline = False)
  embed.set_footer(text = footer_text)

  return embed