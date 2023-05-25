import discord
from utils.config import prefix, debug_channel, debug

description = """Main discord bot file"""


# Configure intents
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

# Create bot object
bot = discord.Client(intents=intents)

# Configure debug channel
debug_channel = bot.get_channel(debug_channel)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    if debug: 
        await debug_channel.send("--- Bot Online ---")


@bot.event
async def on_message(message):
    # Ignores messages sent by the bot
    if message.author == bot.user:
        return

    # Identifies messages that start with the configured prefix
    for char in prefix:
        if message.content.startswith(char):
            # Message without the prefix
            cmd = message.content[1:]
            # Isolates the cog call
            call = cmd.split(" ")[0]
            # Import the cog dynamically
            cog = getattr(__import__('cogs.' + call), call)
            # Call the main function of the cog with the message as the argument
            await cog.main(message)



if __name__ == "__main__":
    token = open(".env/token", "r").read()
    bot.run(token)