import discord
import yt_dlp
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        """Joins a voice channel"""

        if ctx.author.voice and ctx.author.voice.channel is None:
            await ctx.send("You need to be in a voice channel to use this command.")
            return

        # Retrieves the voice channel of the author
        channel = ctx.author.voice.channel

        # Move to the author's channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
    
    @commands.command()
    async def leave(self, ctx):
        """Leaves the voice channel"""
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
    
    @commands.command()
    async def play(self, ctx, url):
        """Plays a song from YouTube"""

        # If not yet in a voice channel, join the author's
        if ctx.voice_client is None:
            await self.join(ctx)

        # Sets the format and postprocessing for the audio
        parameters = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }


        with yt_dlp.YoutubeDL(parameters) as youtube:
            # Extract information about the video specified by the user provided url
            info = youtube.extract_info(url, download=False)
            # Extracts the URL of the first available format for the video
            video_url = info['formats'][0]['url']
            # Stops the currently playing audio in the voice client
            ctx.voice_client.stop()
            # Plays the audio from the provided video_url
            ctx.voice_client.play(discord.FFmpegPCMAudio(video_url))


async def setup(bot):
    await bot.add_cog(Music(bot))