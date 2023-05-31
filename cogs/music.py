import discord
import asyncio
from yt_dlp import YoutubeDL
from discord.utils import get
import utils.config as config
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.current = None
        self.disconnect_timers = {}


    @commands.command(aliases=config.music['join'])
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



    @commands.command(aliases=config.music['leave'])
    async def leave(self, ctx):
        """- Disconnect from the voice channel"""

        # Get the voice client
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        # Disconnect from the voice channel it is in
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()



    @commands.command(aliases=config.music['clear'])
    async def clear(self, ctx):
        """- Stop playing the current song and clears the queue"""
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        # If the voice client is connected and playing, stop the playback
        if voice_client and voice_client.is_playing():
            voice_client.stop()

        # Clear the queue and set the current song to None
        self.queue.clear()
        self.current = None



    @commands.command(aliases=config.music['skip'])
    async def skip(self, ctx):
        """- Skips the current song and plays the next"""
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        
        # Stop the current client
        if voice_client is not None:
            voice_client.stop()

        # If the queue is not empty, call the play_song() function
        if len(self.queue):
            await self.play_song(ctx, skip=True)
        else:
            self.current = None



    @commands.command(aliases=config.music['queue'])
    async def queue(self, ctx):
        """- Shows the current queue"""

        # If the queue is empty, send an embed message indicating that
        if len(self.queue) == 0:
            embed = discord.Embed(description="The queue is empty")
            # If the queue is empty but there is a song playing then display that
            if self.current is not None:
                embed.set_footer(text=f"Currently playing:\n{self.current['title']}")
            await ctx.send(embed=embed)
            return

        # Format the song information for display
        items = ""
        for i, song in enumerate(self.queue):
            title = song['title']
            duration = song['duration']
            minutes, seconds = divmod(duration, 60)
            items += f"`{i+1}.` `[{minutes:02d}:{seconds:02d}]`  {title}\n"

        # Create an embed message with the queue information
        embed = discord.Embed(
            title=f"Queue [{len(self.queue)}]",
            description=f"{items}"
        )

        # Set a footer for any currently playing song if one exists
        if self.current is not None:
            embed.set_footer(text=f"Currently playing:\n{self.current['title']}")

        await ctx.send(embed=embed)



    @commands.command(aliases=config.music['remove'])
    async def remove(self, ctx, index=1):
        """- Remove a song from a given index, assuming the first if not specified"""
        index = int(index)
        try:
            # if the given index is 0, remove the currently playing song
            if index == 0:
                await self.skip(ctx)
                return
            # Remove song at given index
            removed = self.queue.pop(index-1)
            embed = discord.Embed(description=f"Removed {removed['title']} from queue")
            await ctx.send(embed=embed)
        except IndexError:
            return
            # embed = discord.Embed(description=f"Given index `{index}` not in queue")
            # await ctx.send(embed=embed)



    @commands.command(aliases=config.music['play'])
    async def play(self, ctx, *, query=None):
        """- Play a song from YouTube"""

        # Do nothing if query is empty
        if query == None or query == "":
            return
        
        # If song entries are separated by a comma, search and play for all
        if "," in query:
            queries = query.split(",")
            for i in queries:
                await self.play(ctx, query=i)
                print(i)
            return


        # Connect to the author's channel
        await ctx.invoke(self.join)
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        # If a song from a playlist is given, ignore the playlist
        if "&list=" in query:
            query = query.split("&list=")[0]

        # Create and send an embed to confirm the author's input
        embed = discord.Embed(description=f"Adding `{query}` to queue...")
        waiting_message = await ctx.send(embed=embed)

        # parameters for YoutubeDL
        parameters = {
            'noplaylist':           True,
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
        # and ignore if skipping the song
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

        # if skip is True then this will cause an UnboundLocalError and will be caught
        try:
            # Start playing the song using FFmpeg and set the after callback to call this function and play the next song
            voice_client.play(discord.FFmpegPCMAudio(url, **ffmpeg_options), after=lambda e: self.bot.loop.create_task(self.play_song(ctx)))
        except UnboundLocalError:
            # print("skip was invoked")
            pass



    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """- Sets a timer that disconnects the bot if there are no other users in the voice channel"""
        # get the voice channel from the before or after object
        voice_channel = before.channel or after.channel
        if voice_channel:
            # get the number of connected users in the voice channel
            connected_users = len(voice_channel.members) - 1
            # if there are no connected users, initiate the disconnect timer
            if connected_users == 0:
                # cancel the timer if one is already running
                if voice_channel.guild.id in self.disconnect_timers:
                    self.disconnect_timers[voice_channel.guild.id].cancel()
                # set the timer for 4 seconds
                self.disconnect_timers[voice_channel.guild.id] = self.bot.loop.call_later(4, self.disconnect_from_empty_channel, voice_channel)



    def disconnect_from_empty_channel(self, voice_channel):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=voice_channel.guild)
        guild_id = voice_channel.guild.id
        # cancel the active timer
        if guild_id in self.disconnect_timers:
            self.disconnect_timers.pop(guild_id).cancel()

        # disconnect the bot
        if voice_client and voice_client.is_connected() and len(voice_channel.members) == 1:
            self.bot.loop.create_task(voice_client.disconnect())



async def setup(bot):
    await bot.add_cog(Music(bot))