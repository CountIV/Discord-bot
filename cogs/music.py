import discord
from discord.utils import get
from yt_dlp import YoutubeDL
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []


    @commands.command()
    async def join(self, ctx):
        """- Join the voice channel of the author"""
        
        channel = ctx.author.voice.channel
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_connected():
            await voice_client.move_to(channel)
        else:
            voice_client = await channel.connect()


    @commands.command()
    async def leave(self, ctx):
        """- Disconnect from the voice channel"""

        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()


    @commands.command()
    async def play(self, ctx, url):
        """- Play a song from YouTube"""

        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        # Connect to the author's channel
        if not voice_client or not voice_client.is_connected():
            await ctx.invoke(self.join)

        parameters = {
            'format':               'bestaudio/best',
            'postprocessors': [{
                'key':              'FFmpegExtractAudio',
                'preferredcodec':   'mp3',
                'preferredquality': '192',
            }],
        }

        with YoutubeDL(parameters) as youtube:
            info = youtube.extract_info(url, download=False)
            song = info['formats'][0]['url']

        # Add the song to the queue and play it
        self.queue.append(song)

        if not voice_client.is_playing():
            await self.play_song(ctx)


    @commands.command()
    async def clear(self, ctx):
        """- Stop playing the current song and clears the queue"""

        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_playing():
            voice_client.stop()
        
        self.queue.clear()


    async def play_song(self, ctx):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        if not self.queue:
            embed = discord.Embed(description="The queue is empty.")
            await ctx.send(embed=embed)
            return

        current_song = self.queue.pop(0)
        voice_client.play(discord.FFmpegPCMAudio(current_song), after=lambda e: self.bot.loop.create_task(self.play_song(ctx)))


async def setup(bot):
    await bot.add_cog(Music(bot))