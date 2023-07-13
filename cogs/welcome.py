from discord.ext import commands
import random

flavor_text_list = ["blasts into the server!", "catapults into the server!", "teleports into the server!"]

# Gives warm welcome to new members joining the server
class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        flavor_text = random.choice(flavor_text_list)
        await channel.send(f"{member.mention} {flavor_text}")


async def setup(bot):
    await bot.add_cog(Welcome(bot))