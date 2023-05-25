description = """Repeats what you tell it to say."""

async def main(message):
    await message.channel.send(message.content[5:])
    
