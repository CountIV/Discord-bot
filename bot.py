import discord
from utils.config import prefix, log_channel, log_level

description = """Main discord bot file"""


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

                # message = "--- Bot ready ---"
                # await channel.send(message)


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
            # Import the module dynamically
            module = getattr(__import__('modules.' + call), call)
            # Call the main function of the module with the message as the argument
            await module.main(message)



if __name__ == "__main__":
    token = open(".env/token", "r").read()
    bot.run(token)