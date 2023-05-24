import discord
import glob
import importlib
from utils.config import prefix, log_channel, log_level

# Get a list of all modules within the folder
modules = glob.glob("modules/*.py")

# Imports all modules dynamically
for m in modules:
    module_name = m[:-3].replace('\\', '.')
    module = importlib.import_module(module_name)
    globals().update(vars(module))

# Configure intents
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

# Create bot object
bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print()
    
    # Find the log channel from every server the bot is in
    for guild in bot.guilds:
        for channel in guild.text_channels:
            # Sends a "Bot ready." message to the log channel
            if channel.name == log_channel:
                global log
                log = channel

                message = "--- Bot ready ---"
                await channel.send(message)


@bot.event
async def on_message(message):
    # Ignores messages sent by the bot
    if message.author == bot.user:
        return
    else:
        if log_level[0]: 
            auth = message.author
            await log.send('Recieved from: ' + auth.name + '#' + auth.discriminator + '\nWith message: ' + message.content)

    # Identifies messages that start with the configured prefix
    for char in prefix:
        if message.content.startswith(char):
            if log_level[0]: await message.channel.send('Command read: ' + message.content[1:])
            # Message without the prefix
            cmd = message.content[1:]
            # Isolates the module call
            call = cmd.split(" ")[0]
            # Call the function with the message as the arg
            function = getattr(__import__('modules.' + call), call)
            await function.main(message)



token = open(".env/token", "r").read()
bot.run(token)