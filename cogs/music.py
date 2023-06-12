import random
import discord
from yt_dlp import YoutubeDL
from discord.utils import get
import utils.config as config
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.loop = False
        self.current_item = None
        self.now_playing = None
        self.disconnect_timers = {}


    @commands.command(aliases=config.music['join'])
    async def join(self, ctx):
        """Joins the voice channel of the user who issued the command."""

        # Get the voice channel of the user who issued the command
        channel = ctx.author.voice.channel

        # If the bot is already connected to a voice channel, move it to the new one
        if ctx.voice_client and ctx.voice_client.is_connected():
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()


    @commands.command(aliases=config.music['leave'])
    async def leave(self, ctx):
        """Disconnects from the voice channel."""

        # Get the voice client
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)

        # Disconnect from the voice channel it is in
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()


    @commands.command(aliases=config.music['clear'])
    async def clear(self, ctx):
        """Stops the current song playback and clears the queue."""

        # If the voice client is connected and playing, stop the playback
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        # Clear the queue and set the current song to None
        self.queue.clear()
        self.current_item = None
        await self.bot.change_presence(activity=None)

        # Delete the previous message containing the currently playing song if it exists
        if self.now_playing is not None:
            try:
                await self.now_playing.delete()
            except:
                pass


    @commands.command(aliases=config.music['skip'])
    async def skip(self, ctx):
        """Skips the current song and plays the next one in the queue."""

        # If there is a song currently playng, send an embed informing of the skip
        if self.current_item is not None:
            embed = discord.Embed(description=f"Skipping: **{self.current_item['title']}**")
            await ctx.send(embed=embed)

        # Stop the current client
        if ctx.voice_client is not None:
            ctx.voice_client.stop()

        # If the queue is not empty, call the play_song() function
        if len(self.queue):
            await self.play_song(ctx, skip=True)
        else:
            await self.bot.change_presence(activity=None)
            self.current_item = None


    @commands.command(aliases=config.music['queue'])
    async def queue(self, ctx):
        """Displays the currently playing song and the queue."""

        # If the queue is empty, send an embed message indicating that
        if len(self.queue) == 0:
            embed = discord.Embed(description="The queue is empty")

            # If there there is a song playing then display that
            if self.current_item is not None:
                embed.set_footer(text    =f"Currently playing:\n{self.current_item['title']}",
                                 icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=embed)
            return

        # Format the song information for display
        items = ""
        for i, song in enumerate(self.queue):
            title = song['title']
            duration = song['duration']
            minutes, seconds = divmod(duration, 60)
            items += f"`{(i+1):2d}.` `[{minutes:02d}:{seconds:02d}]`  {title}\n"

            # If the queue is too long, only display as many songs as will fit in a message
            if len(items) > 1800:
                title = self.queue[-1]['title']
                duration = self.queue[-1]['duration']
                minutes, seconds = divmod(duration, 60)
                items += f" •\n •\n •\n`{len(self.queue)}.` `[{minutes:02d}:{seconds:02d}]`  {title}\n"
                break

        # Create an embed message with the queue information
        embed = discord.Embed(title      =f"Queue [{len(self.queue)}]",
                              description=f"{items}",)

        # Set a footer for any currently playing song if one exists
        if self.current_item is not None:
            embed.set_footer(text    =f"Currently playing:\n{self.current_item['title']}",
                             icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)


    @commands.command(aliases=config.music['remove'])
    async def remove(self, ctx, index=-1):
        """Removes a song from the queue at the given index. If no index is specified, it removes the last added song."""
        index = int(index)
        try:
            # if the given index is 0, remove the currently playing song
            if index == 0:
                await self.skip(ctx)
                return

            # Remove song at given index
            if index > 0:
                removed = self.queue.pop(index-1)
            else:
                removed = self.queue.pop(index)

            embed = discord.Embed(description=f"Removed {removed['title']} from queue")
            await ctx.send(embed=embed)
        except IndexError:
            return


    @commands.command(aliases=config.music['loop'])
    async def loop(self, ctx):
        """Enables looping of the current queue, excluding the currently playing song."""

        # Set the loop variable to the opposite of what it currently is and send an embed message informing of the change
        self.loop = not self.loop
        embed = discord.Embed(description=f"Looping is now `{self.loop}`")
        await ctx.send(embed=embed)


    @commands.command(aliases=config.music['move'])
    async def move(self, ctx, index1, index2):
        """Moves a song from one position in the queue to another."""

        index1, index2 = int(index1), int(index2)

        # If the given indices are the same, do nothing
        if index1 == index2:
            return

        # If one of the indices is 0, tell the user that they cannot move the currently playing song
        if index1 == 0 or index2 == 0:
            embed = discord.Embed(description=f"Cannot move currently playing song")
            await ctx.send(embed=embed)
            return

        # Move the song from index1 to index2
        try:
            song = self.queue.pop(index1-1)
            self.queue.insert(index2-1, song)
            embed = discord.Embed(description=f"Moved `{song['title']}` from `{index1}.` to `{index2}.`")
            await ctx.send(embed=embed)
        except IndexError:
            embed = discord.Embed(description=f"Given index not in queue")
            await ctx.send(embed=embed)


    @commands.command(aliases=config.music['shuffle'])
    async def shuffle(self, ctx):
        """Shuffles the queue."""

        # Shuffle the queue and send an embed message informing of the shuffle
        random.shuffle(self.queue)
        embed = discord.Embed(description=f"Shuffled queue")
        await ctx.send(embed=embed)


    @commands.command(aliases=config.music['playlist'])
    async def playlist(self, ctx, *, code=None):
        """Convert the current queue into a playlist code. If a code is provided, play the corresponding playlist."""

        # If a code is not provided, create a playlist code from the queue
        if code is None:
            # If the queue is empty, do nothing
            if len(self.queue) == 0:
                embed = discord.Embed(description="The queue is empty")
                await ctx.send(embed=embed)
                return

            # Create a playlist code from the queue
            code = f"{self.current_item['id']}"
            for song in self.queue:
                code += f"{song['id']}"

            # Send the playlist code
            await ctx.send(f"Playlist code:\n```yaml\n{code}<>```")
        else:
            # If the playlist code is invalid, do nothing
            if len(code) % 11 != 2 and "<>" not in code:
                embed = discord.Embed(description="Invalid playlist code",
                                      color      =discord.Color.red())
                await ctx.send(embed=embed)
                return

            # Convert the playlist code into a list of song urls
            playlist = ""
            for i in range(0, len(code)-2, 11):
                playlist += f"https://www.youtube.com/watch?v={code[i:i+11]}, "

            # Add the songs to the queue
            await self.play(ctx, index="-1", song=playlist)


    @commands.command(aliases=config.music['play'])
    async def play(self, ctx, index="-1", *, song=""):
        """Plays a requested song. Optionally, specify an index to add the song to the queue at a specific position."""

        # Connect to the author's channel
        await ctx.invoke(self.join)

        # If the index is not an integer, assume that the query is the index and the index is -1
        try:
            index = int(index) if index == "-1" else int(index) - 1
        except ValueError:
            song = f"{index.strip()} {song.strip()}"
            index = -1

        # If the index is larger than the queue, set it to the last index
        if int(index) > len(self.queue):
            index = -1

        # Do nothing if query is empty
        if song.strip() == "":
            return

        # If song entries are separated by a comma, search and play for all
        if "," in song:
            queries = song.split(",")
            for i in queries:
                await self.play(ctx, song=i.strip())
            return

        # If a is provided with an attached playlist, ignore the playlist
        if "&list=" in song:
            song = song.split("&list=")[0]

        # Send a message saying that the song is being added to the queue
        if "https://www.youtube.com/watch?v=" in song:
            temp_msg = await ctx.send(f"Adding to queue...")
        else:
            temp_msg = await ctx.send(f"Adding `{song}` to queue...")

        # Get the song info
        item = await self.get_item(ctx, song)
        if item is None:
            await temp_msg.delete()
            embed = discord.Embed(description=f"No videos found with `{song}`")
            await ctx.send(embed=embed)
            return

        # Get song duration and format it to mm:ss
        m, s = divmod(item['duration'], 60)
        duration = f"{m:02d}:{s:02d}"

        # Display serached song info
        if index == -1:
            i = len(self.queue) + 1 if self.current_item is not None else len(self.queue)
        else:
            i = index + 1

        await temp_msg.delete()

        # Send a message saying that the song has been added to the queue
        if i != 0:
            await ctx.send(f"`{i:2d}.` `[{duration}]` **{item['title']}**")

        # Add song to the queue
        self.queue.append(item) if index == -1 else self.queue.insert(index, item)

        # Play the song if none are currently playing
        if not ctx.voice_client.is_playing() and self.current_item is None:
            await self.play_song(ctx)


    async def get_item(self, ctx, query):
        """Returns a dictionary containing the requested song's info."""

        # parameters for YoutubeDL
        parameters = {'noplaylist':           True,
                      'default_search':       'ytsearch',
                      'format':               'bestaudio/best',
                      'postprocessors':       [{'key':              'FFmpegExtractAudio',
                                                'preferredcodec':   'mp3',
                                                'preferredquality': '192',}],
                      'youtube_include_dash_manifest': False}

        # Get requested song url and title
        try:
            with YoutubeDL(parameters) as youtube:
                # Search and return the first result found
                print("―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――")
                info = youtube.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
                print("―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――")
                # Collect only relevant info
                item = {'id':           info['id'],         # Video id
                        'url':          info['url'],        # Video url
                        'title':        info['title'],      # Video title
                        'duration':     info['duration'],   # Video duration in seconds
                        'uploader':     info['uploader'],   # Video uploader
                        'thumbnail':    info['thumbnail'],  # Video thumbnail
                        'requester':    ctx.author,         # Video requester
                }
        except IndexError:
                return None
        return item


    async def play_song(self, ctx, skip=False):
        # Delete the previous message containing the currently playing song if it exists
        if self.now_playing is not None:
            try:    await self.now_playing.delete()
            except: pass
        else:
            await self.bot.change_presence(activity=None)

        # If the queue is empty, send the relevant response
        if not self.queue:
            embed = discord.Embed(description="The queue is now empty")
            await self.bot.change_presence(activity=None)
            await ctx.send(embed=embed)
            return

        if not skip:
            # Retrieve the information of the current song from the queue
            # and ignore if skipping the song
            song = self.queue.pop(0)

            url       = song['url']
            title     = song['title']
            uploader  = song['uploader']
            requester = song['requester']
            thumbnail = song['thumbnail']
            self.current_item = song

            # If looping is enabled, add the current song back to the queue
            if self.loop is True:
                self.queue.append(song)

            # Create an embed message to display the current song being played
            embed = discord.Embed(title      =f"Now playing: **{title}**",
                                  description=f"**{uploader}**",
                                  color      =16711680)
            embed.set_footer(text    =f"Requested by {requester}",
                             icon_url=ctx.author.display_avatar.url)
            embed.set_thumbnail(url=thumbnail)
            self.now_playing = await ctx.send(embed=embed)

        # Options to reconnect rather than terminate song if disconnected by corrupt packets
        ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn',}

        try:
            # Set the bot's status to the current song
            await self.bot.change_presence(activity=discord.Activity(name=title,
                                                                     type=discord.ActivityType.playing,
                                                                     state="",
                                                                     url=f"https://www.youtube.com/watch?v={song['id']}",))

            # Start playing the song using FFmpeg and set the after callback to call this function and play the next song
            ctx.voice_client.play(discord.FFmpegPCMAudio(url, **ffmpeg_options), after=lambda e: self.bot.loop.create_task(self.play_song(ctx)))
        except UnboundLocalError:
            pass


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Sets a timer that disconnects the bot if there are no other users in the voice channel"""
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