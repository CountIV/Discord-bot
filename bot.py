import time
import discord
import os
from discord.ext import commands
from utils.config import prefix, admin_role


# Create bot object
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())



@bot.event
async def on_ready():
    # List of cog files within the cogs folder
    cog_files = [f for f in os.listdir('cogs') if f.endswith('.py')]
    
    # Load cogs
    for cog in cog_files:
        extension = f"cogs.{cog[:-3]}"
        try:
            await bot.load_extension(extension)
        except Exception as e:
            print(e)
    
    print(f'Logged in as {bot.user}')



@bot.event
async def on_member_join(member):
    # Gives warm welcome to new members
    channel = member.guild.system_channel
    await channel.send(f"{member.mention} blasts into the server!")



@bot.command()
@commands.has_role(admin_role)
async def restart(ctx):
    """Restarts all cogs"""
    start_time = time.time()
    embed = discord.Embed(title=f"Restarting...", color=discord.Color.red())
    waiting = await ctx.send(embed=embed)
    cog_files = [f for f in os.listdir('cogs') if f.endswith('.py')]
    errors = ""
    for cog in cog_files:
        extension = f"cogs.{cog[:-3]}"
        try:
            await bot.reload_extension(extension)
        except Exception as e:
            try:
                await bot.load_extension(extension)
            except Exception as e:
                errors += f"{e}\n"

    embed = discord.Embed(title       = f"**{bot.user.name}** has been rebooted", color=discord.Color.green(), 
                          description = f"```yaml\n{errors}```" if errors else "")

    elapsed_time = time.time() - start_time
    elapsed_time_formatted = f"{elapsed_time:.2f}s"
    embed.set_footer(text=f"Boot time: {elapsed_time_formatted}")

    await waiting.edit(embed=embed)



if __name__ == "__main__":
    token = open(".env/token", "r").read()
    bot.run(token)