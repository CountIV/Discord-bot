async def main(message):
    await message.channel.send(message.content[1:].split('say ')[1])
    
