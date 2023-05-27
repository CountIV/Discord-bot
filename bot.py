import discord
import os
from discord.ext import commands
from utils.config import prefix


# Create bot object
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())


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
        except Exception as e:
            print(e)


@bot.event
async def on_member_join(member):
    # Gives warm welcome to new members
    channel = member.guild.system_channel
    await channel.send(f"{member.mention} blasts into the server!")


if __name__ == "__main__":
    token = open(".env/token", "r").read()
    bot.run(token)