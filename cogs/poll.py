import discord
from discord.ext import commands


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.poll_host = None
        self.current_poll = None


    @commands.command()
    async def poll(self, ctx, *, entries="2"):
        """Creates a poll with the given comma separated entries. Optionally, you can specify the number of entries to create."""

        # Split the entries into a list
        if entries.isnumeric():
            entries = [None for _ in range(int(entries))]
        else:
            entries = entries.split(",")

        # Check if the number of entries is valid
        if len(entries) > 18:
            await ctx.send("Too many entries.")
            return

        # Create the embed
        embed = discord.Embed(title="",
                              description="",
                              color=discord.Color.blue())
        embed.set_footer(icon_url=ctx.author.display_avatar.url)

        # Add the entries to the embed
        for i, entry in enumerate(entries):
            entry = f" {entry.strip()}" if entry is not None else f""
            embed.add_field(name=f"{chr(127462+i)} |{entry}", value="", inline=True)
        embed.set_author(name="Poll", icon_url=ctx.guild.icon.url)

        # Send the embed
        message = await ctx.send(embed=embed)

        # Add reactions to the message
        for i in range(len(entries)):
            await message.add_reaction(chr(127462+i))
        await message.add_reaction(chr(0x274C))

        self.poll_host = ctx.author
        self.current_poll = message


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        # Rejection conditions
        if self.current_poll is None:
            return
        if reaction.message.id != self.current_poll.id:
            return
        if user == self.bot.user:
            return
        if user != self.poll_host and reaction.emoji == chr(0x274C):
            await reaction.message.remove_reaction(reaction, user)
            return

        # Check if the :x: reaction is on the current poll
        if reaction.emoji != chr(0x274C):
            return

        # Get all the names in the fields of the poll
        names = [field.name for field in reaction.message.embeds[0].fields]
        names = { name.split("|")[0].strip():name.split("|")[1].strip() for name in names }

        # Create the embed
        embed = discord.Embed(color=discord.Color.dark_green())
        embed.set_author(name="Poll ended")

        # Add the results to the embed
        for reaction in reaction.message.reactions:
            if reaction.emoji != chr(0x274C):
                # Highlight the most popular option
                if reaction.count == max([r.count for r in reaction.message.reactions]):
                    count = f"```{reaction.count-1:2d} ✅```"
                else:
                    count = f"```{(reaction.count-1):2d} ```"

                # Format the results
                title = names[reaction.emoji] if names[reaction.emoji] != "" else reaction.emoji
                embed.add_field(name=f"{title}: {count}", value=f"", inline=True)

        # Remove all reactions and update the message
        await reaction.message.clear_reactions()
        await reaction.message.edit(embed=embed)



async def setup(bot):
    await bot.add_cog(Poll(bot))