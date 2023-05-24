import discord
from utils.config import prefix, log_channel, log_level


intents = discord.Intents.default()
bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
    # Find the log channel from every server the bot is in
    for guild in bot.guilds:
        for channel in guild.text_channels:
            # Sends a "Bot ready." message to the log channel
            if channel.name == log_channel:
                message = "Bot ready."
                await channel.send(message)




token = open(".env/token", "r").read()
bot.run(token)