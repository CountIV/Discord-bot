import discord
import os
from discord.ext import commands
from utils.config import prefix


description = """Main discord bot file"""


# Configure intents
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True


# Create bot object
bot = commands.Bot(command_prefix=prefix, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    # List of cog files within the cogs folder
    cog_files = [f for f in os.listdir('cogs') if f.endswith('.py')]
    
    # Load cogs
    for cog in cog_files:
        extension = f"cogs.{cog[:-3]}"
        try:
            await bot.load_extension(extension)
        except:
            pass


if __name__ == "__main__":
    token = open(".env/token", "r").read()
    bot.run(token)