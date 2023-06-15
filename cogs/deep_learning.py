from discord.ext import commands
import requests
from io import BytesIO
from utils.digit_classification import digit_classification

class Deep_Learning(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ai(self, ctx, message):
        """Utilizes deep learning to recognize digits in image format."""
        url = message
        # Only accept discord links
        if url[0:26] == "https://cdn.discordapp.com":
            response = requests.get(url)
            image = BytesIO(response.content)
            result = "That digit looks like " + str(digit_classification(image))
        else:
            result = "Invalid input, please send discord image"

        await ctx.send(result)

async def setup(bot):
    await bot.add_cog(Deep_Learning(bot))