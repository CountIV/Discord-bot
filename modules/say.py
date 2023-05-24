async def main(message):
    await message.channel.send(message.content[5:])
    
