import discord

async def main(message):
    await message.channel.send(message.content.split('!say ')[1])
    
