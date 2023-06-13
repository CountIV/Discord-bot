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

    # Set bot status
    await bot.change_presence(activity=None)
    print(f'Logged in as {bot.user}')


@bot.event
async def on_member_join(member):
    # Gives warm welcome to new members
    channel = member.guild.system_channel
    await channel.send(f"{member.mention} blasts into the server!")


@bot.command(aliases=["install"], hidden=True)
@commands.has_role(admin_role)
async def load(ctx, target_cog=None):
    """Loads a cog."""

    # Start timer
    start_time = time.time()

    # List of cog files within the cogs folder
    cog_files = [f for f in os.listdir('cogs') if f.endswith('.py')]
    if target_cog is not None:
        cog_files = [f"{target_cog}.py"]

    # send message to indicate that the cog is being loaded
    embed = discord.Embed(title=f"Loading...", color=discord.Color.red())
    waiting = await ctx.send(embed=embed)

    errors = ""
    success = []
    # Load cogs
    for cog in cog_files:
        extension = f"cogs.{cog[:-3]}"
        try:
            await bot.load_extension(extension)
            success.append(cog)
        except Exception as e:
            errors += f"{e}\n"

    success = " ".join(success)

    # Configure embed to indicate that the cog has been loaded
    target = f"**{target_cog}** has been loaded" if target_cog is not None else f"Loaded ```{success}```"
    embed = discord.Embed(title      =f"{target}",
                          description=f"With errors:```yaml\n{errors}```" if errors else "",
                          color      =discord.Color.green())

    # Add elapsed time to footer
    elapsed_time = time.time() - start_time
    elapsed_time_formatted = f"{elapsed_time:.2f}s"
    embed.set_footer(text=f"Load time: {elapsed_time_formatted}")

    print(f"{'―' * 32}\n{target} in {elapsed_time_formatted}")

    await waiting.edit(embed=embed)


@bot.command(aliases=["uninstall"], hidden=True)
@commands.has_role(admin_role)
async def unload(ctx, target_cog=None):
    """Unloads a cog."""

    # Start timer
    start_time = time.time()

    # Stops any playing audio if the target_cog is music
    if target_cog == "music" and ctx.voice_client and ctx.voice_client.is_playing():
            await ctx.invoke(bot.get_command("clear"))

    # List of cog files within the cogs folder
    cog_files = [f for f in os.listdir('cogs') if f.endswith('.py')]
    if target_cog is not None:
        cog_files = [f"{target_cog}.py"]

    # send message to indicate that the cog is being unloaded
    embed = discord.Embed(title=f"Unloading...", color=discord.Color.red())
    waiting = await ctx.send(embed=embed)

    errors = ""
    success = []
    # Unload cogs
    for cog in cog_files:
        extension = f"cogs.{cog[:-3]}"
        try:
            if cog == "help.py":
                continue
            await bot.unload_extension(extension)
            success.append(cog)
        except Exception as e:
            errors += f"{e}\n"

    success = " ".join(success)

    # Configure embed to indicate that the cog has been unloaded
    target = f"**{target_cog}** has been unloaded" if target_cog is not None else f"Unloaded ```{success}```"
    embed = discord.Embed(title      =f"{target}",
                          description=f"With errors:```yaml\n{errors}```" if errors else "",
                          color      =discord.Color.green())

    # Add elapsed time to footer
    elapsed_time = time.time() - start_time
    elapsed_time_formatted = f"{elapsed_time:.2f}s"
    embed.set_footer(text=f"Unload time: {elapsed_time_formatted}")

    print(f"{'―' * 32}\n{target} in {elapsed_time_formatted}")

    await waiting.edit(embed=embed)


@bot.command(aliases=["reload", "reboot", "re"], hidden=True)
@commands.has_role(admin_role)
async def restart(ctx, target_cog=None):
    """Restarts all cogs."""

    # Start timer
    start_time = time.time()

    # Stops any playing audio if the target_cog is music
    if target_cog == "music" and ctx.voice_client and ctx.voice_client.is_playing():
            await ctx.invoke(bot.get_command("clear"))

    # Send message to indicate that the bot is restarting
    embed = discord.Embed(title=f"Restarting...", color=discord.Color.red())
    waiting = await ctx.send(embed=embed)

    # List of cog files within the cogs folder
    cog_files = [f for f in os.listdir('cogs') if f.endswith('.py')]
    if target_cog is not None:
        cog_files = [f"{target_cog}.py"]

    errors = ""
    # Reload cogs
    for cog in cog_files:
        extension = f"cogs.{cog[:-3]}"
        try:
            await bot.reload_extension(extension)
        except Exception as e:
            try:
                await bot.load_extension(extension)
            except Exception as e:
                errors += f"{e}\n"

    # Set bot status
    await bot.change_presence(activity=None, status=discord.Status.online)

    # Send message to indicate that the bot has been restarted
    target = f"{target_cog}" if target_cog is not None else f"{bot.user.name}"
    embed = discord.Embed(title       = f"**{target}** has been rebooted", color=discord.Color.green(),
                          description = f"With errors:```yaml\n{errors}```" if errors else "")

    # Add elapsed time to footer
    elapsed_time = time.time() - start_time
    elapsed_time_formatted = f"{elapsed_time:.2f}s"
    embed.set_footer(text=f"Reboot time: {elapsed_time_formatted}")

    print(f"{'―' * 32}\nRebooted {target} in {elapsed_time_formatted}")

    await waiting.edit(embed=embed)


if __name__ == "__main__":
    token = open(".env/token", "r").read()
    bot.run(token)