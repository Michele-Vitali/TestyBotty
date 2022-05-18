import discord
from discord.ext import commands
import re
import youtube_dl

class music(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    print('Music cog loaded')

  @commands.command(name = 'leave', aliases = ['l'])
  async def leave(self, ctx):
    await ctx.voice_client.disconnect()

  @commands.command(name = 'join', aliases = ['j'])
  async def join(self, ctx):
    if ctx.author.voice is not None:
      voice_channel = ctx.author.voice.channel
      if ctx.voice_client is None:
        await voice_channel.connect()
        await ctx.send("Connected to the channel!")
      else:
        await ctx.voice_client.move_to(voice_channel)
        await ctx.send("Moved to the channel!")
    else:
      await ctx.send("You're not in any voice channel, join one please")
  
  @commands.command(name = 'play', aliases = ['p'])
  async def play(self, ctx, url):
    spotify_regex = r"[\bhttps://open.\b]*spotify[\b.com\b]*[/:]*track[/:]*[A-Za-z0-9]+"
    youtube_regex = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
    check_if_spotify = re.findall(spotify_regex, url)
    check_if_youtube = re.findall(youtube_regex, url)
    print("Youtube: ", check_if_youtube)
    print("Spotify: ", check_if_spotify)

    ctx.voice_client.stop()
    FFMPEG_OPTIONS = {'before_options' : '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options' : '-vn'}
    YDL_OPTIONS = {'format' : 'bestaudio'}

    vc = ctx.voice_client
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download = False)
      link = info['formats'][0]['url']
      source = await discord.FFmpegOpusAudio.from_probe(link, **FFMPEG_OPTIONS)
      vc.play(source)
      await ctx.send(f"Now playing {source.title}")

  @commands.command(name = 'stop', aliases = ['s'])
  async def stop(self, ctx):
    await ctx.voice_client.pause()
    await ctx.send("Paused")

  @commands.command(name = 'resume', aliases = ['r'])
  async def resume(self, ctx):
    await ctx.voice_client.resume()
    await ctx.send("Paused")

def setup(bot):
  bot.add_cog(music(bot))