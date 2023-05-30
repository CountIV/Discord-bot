import discord
from yt_dlp import YoutubeDL
from discord.utils import get
import utils.config as config
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.current = None


    @commands.command(aliases=config.music_join)
    async def join(self, ctx):
        """- Join the voice channel of the author"""
        
        # Get the voice channel of the author
        channel = ctx.author.voice.channel

        # Get the voice client of the bot in the guild
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        # Check if the bot is already connected to a voice channel 
        # and either move or connect to the author's voice channel
        if voice_client and voice_client.is_connected():
            await voice_client.move_to(channel)
        else:
            voice_client = await channel.connect()


    @commands.command(aliases=config.music_leave)
    async def leave(self, ctx):
        """- Disconnect from the voice channel"""

        # Get the voice client
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        # Disconnect from the voice channel it is in
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()


    @commands.command(aliases=config.music_play)
    async def play(self, ctx, *, query):
        """- Play a song from YouTube"""

        # Connect to the author's channel
        await ctx.invoke(self.join)
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        # Create and send an embed to confirm the author's input
        embed = discord.Embed(description=f"Adding `{query}` to queue...")
        waiting_message = await ctx.send(embed=embed)

        # parameters for YoutubeDL
        parameters = {
            'noplaylist':           True,
            # 'quiet':                False,
            'default_search':       'ytsearch',
            'format':               'bestaudio/best',
            'postprocessors': [{
                'key':              'FFmpegExtractAudio',
                'preferredcodec':   'mp3',
                'preferredquality': '192',
            }],
            'youtube_include_dash_manifest': False
        }

        # Get requested song url and title
        try:
            with YoutubeDL(parameters) as youtube:
                # Search and return the first result found
                info = youtube.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
                info = youtube.sanitize_info(info)
                # Collect only relevant info
                item = {
                    'url':          info['url'], 
                    'title':        info['title'], 
                    'duration':     info['duration'], 
                    'uploader':     info['uploader'],
                    'requester':    ctx.author,
            }
        except IndexError:
                # If no videos found, send an error message and return
                embed = discord.Embed(description=f"No videos found with `{query}`")
                await ctx.send(embed=embed)
                await waiting_message.delete()
                return

        # Get song duration and format it to mm:ss
        minutes, seconds = divmod(item['duration'], 60)
        duration = f"{minutes:02d}:{seconds:02d}"

        # Display serached song info
        embed = discord.Embed(description=f"`{len(self.queue) + 1}.` `[{duration}]` **{item['title']}**")
        await waiting_message.delete()
        await ctx.send(embed=embed)

        # Add song to the queue
        self.queue.append(item)

        # Play the song if none are currently playing
        if not voice_client.is_playing():
            await self.play_song(ctx)


    @commands.command(aliases=config.music_clear)
    async def clear(self, ctx):
        """- Stop playing the current song and clears the queue"""

        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_playing():
            voice_client.stop()

        self.queue.clear()
        self.current = None


    @commands.command(aliases=config.music_skip)
    async def skip(self, ctx):
        """- Skips the current song and plays the next"""
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        
        # Stop the current client
        voice_client.stop()

        # If the queue is not empty, call the play_song() function
        if len(self.queue):
            await self.play_song(ctx, skip=True)


    @commands.command(aliases=config.music_queue)
    async def queue(self, ctx):
        """- Shows the current queue"""

        # If the queue is empty, send an embed message indicating that
        if len(self.queue) == 0:
            embed = discord.Embed(description="The queue is empty")
            if self.current is not None:
                embed.set_footer(text=f"Currently playing:\n{self.current['title']}")
            await ctx.send(embed=embed)
            return

        items = ""
        for i, song in enumerate(self.queue):
            # Format the song information for display
            title = song['title']
            duration = song['duration']
            minutes, seconds = divmod(duration, 60)
            items += f"`{i+1}.` `[{minutes:02d}:{seconds:02d}]`  {title}\n"

        # Create an embed message with the queue information
        embed = discord.Embed(
            title=f"Queue [{len(self.queue)}]",
            description=f"{items}"
        )
        if self.current is not None:
            embed.set_footer(text=f"Currently playing:\n{self.current['title']}")

        await ctx.send(embed=embed)
    

    @commands.command(alias=config.music_remove)
    async def remove(self, ctx, index=1):
        """- Remove a song from a given index, assume the first if not specified"""
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        removed = self.queue.pop(index)
        embed = discord.Embed(description=f"Removed {removed['title']} from queue")
        await ctx.send(embed=embed)


    async def play_song(self, ctx, skip=False):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        # If the queue is empty, send the relevant response
        if not self.queue:
            embed = discord.Embed(description="The queue is now empty")
            await ctx.send(embed=embed)
            return

        # Options to reconnect rather than terminate song if disconnected by corrupt packets
        ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
        }

        # Retrieve the information of the current song from the queue
        if not skip:
            current_song = self.queue.pop(0)
            self.current = current_song
            url       = current_song['url']
            title     = current_song['title']
            uploader  = current_song['uploader']
            requester = current_song['requester']

            # Create an embed message to display the current song being played
            embed = discord.Embed(
                title=f"Now playing: **{title}**",
                description=f"**{uploader}**",
                color = 16711680
            )
            embed.set_footer(text=f"Requested by {requester}")
            await ctx.send(embed=embed)

        try:
            # Start playing the song using FFmpeg and set the after callback to call this function and play the next song
            voice_client.play(discord.FFmpegPCMAudio(url, **ffmpeg_options), after=lambda e: self.bot.loop.create_task(self.play_song(ctx)))
        except UnboundLocalError:
            # print("skip was invoked")
            pass


async def setup(bot):
    await bot.add_cog(Music(bot))