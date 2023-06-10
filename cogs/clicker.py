import discord
from discord.ext import commands


# Create a custom View class that extends discord.ui.View
class ViewButton(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.score = 0 # Initialize score that keeps track of how many times button has been clicked


    # Define a button interaction handler that increases the score by one every click
    @discord.ui.button(label="🍪", style=discord.ButtonStyle.blurple)
    async def display(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.score += 1 # Adds one to score

        # Creates an embed that displays the score
        embed = discord.Embed(
            title= "Clicker",
            description = self.score
        )
        await interaction.response.edit_message(embed=embed)



class Clicker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["cookie", "🍪"])
    async def clicker(self, ctx):
        """A simple clicker game"""

        # Creates an instance of the ViewButton class
        view = ViewButton()

        await ctx.send(view=view)



async def setup(bot):
    await bot.add_cog(Clicker(bot))