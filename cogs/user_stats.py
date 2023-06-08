import re
import time
import discord
from collections import Counter
from discord.ext import commands



class Users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def stats(self, ctx, user: discord.User):
        """- Display messaging stats for a user"""

        # Start logging the time used to calculate the user's stats
        start_time = time.time()

        embed = discord.Embed(description=f"Calculating user {user}'s message stats...")
        waiting_message = await ctx.send(embed=embed)

        messages = 0
        words = 0
        emojis = 0
        images = 0
        videos = 0
        reactions = 0
        active_period_counts = [0] * 12  # Initialize counts for each 2-hour period
        word_counter = Counter()
        emoji_counter = Counter()

        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                async for message in channel.history(limit=None):
                    if message.author == user:
                        messages += 1
                        words += len(message.content.split())

                        # - Count emojis using regular expressions -
                        # Emoticons and smileys
                        # Flags of different countries
                        # Miscellaneous symbols and pictographs
                        # Various symbols and geometric shapes
                        # Supplemental symbols and pictographs
                        # Transport and map symbols
                        # Enclosed characters and country flags
                        # Custom Discord emojis
                        emoji_pattern = re.compile("[\U0001F600-\U0001F6FF]|[\U0001F1E0-\U0001F1FF]|[\U00002600-\U000027BF]|[\U0001F300-\U0001F5FF]|[\U0001F900-\U0001F9FF]|[\U0001F680-\U0001F6FF]|[\U0001F190-\U0001F1FF]|<:[a-zA-Z0-9_]+:[0-9]+>")
                        emojis += len(emoji_pattern.findall(message.content))

                        word_counter.update(message.content.lower().split())
                        emoji_counter.update(emoji_pattern.findall(message.content))

                        # Count images and videos
                        for attachment in message.attachments:
                            if attachment.filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
                                images += 1
                            elif attachment.filename.endswith((".mp4", ".mov", ".avi")):
                                videos += 1

                        # Count reactions recieved
                        reactions += len(message.reactions)

                        # Record message creation time
                        active_period = message.created_at.hour // 2
                        active_period_counts[active_period] += 1

        # Calculate the most active 2-hour period of the user
        most_active_period = active_period_counts.index(max(active_period_counts))
        active_start_hour = most_active_period * 2
        active_end_hour = active_start_hour + 1

        # Get the top 3 and top 8 most used words and emojis
        top_words = word_counter.most_common(3)
        top_emojis = emoji_counter.most_common(8)

        if top_words:
            top_words_str = ", ".join([f"`{word}`" for word, count in top_words])

        if top_emojis:
            top_emojis_str = "\n".join([f"`{count}`x {emoji}" for emoji, count in top_emojis])

        # Build the embed
        embed = discord.Embed(title="Messaging Stats", color=discord.Color.green())
        embed.add_field(name="User",                value=user.name)
        embed.add_field(name="Messages sent",       value=messages)
        embed.add_field(name="Word count",          value=words)
        embed.add_field(name="Emojis used",         value=emojis)
        embed.add_field(name="Images sent",         value=images)
        embed.add_field(name="Videos sent",         value=videos)
        embed.add_field(name="Reactions received",  value=reactions)
        embed.add_field(name="Most Active Period",  value=f"{active_start_hour:02}:00 - {active_end_hour+1:02}:00")
        embed.add_field(name="Most Used Words",     value=top_words_str)
        embed.add_field(name="Most Used Emojis",    value=top_emojis_str)

        elapsed_time = time.time() - start_time
        elapsed_time_formatted = f"{elapsed_time:.2f}s"  # Format the elapsed time to two decimal places

        embed.set_footer(text=f"Calculation time: {elapsed_time_formatted}")

        await waiting_message.edit(embed=embed)



async def setup(bot):
    await bot.add_cog(Users(bot))