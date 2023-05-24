import discord

intents = discord.Intents.default()
client = discord.Client(intents=intents)





token = open(".env/token", "r").read()
client.run(token)