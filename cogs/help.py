import discord
import glob

description = """This prompt."""

async def main(message):
    # Find all cog files in the 'cogs' folder
    cogs = glob.glob("cogs\*.py")
    commands = [cog[:-3] for cog in cogs]

     # Iterate over each command
    cmd_list = []
    for command in commands:
        # Replace backslashes with dots to create cog name
        cog = command.replace("\\", ".")
        # Add the description of the command from the cog
        command += "\n"+getattr(__import__(cog, fromlist=['']), "description")
        cmd_list.append(command)
    
    # Remove the 'cogs\' prefix from the commands
    cmd_list = [i.replace("cogs\\", "") for i in cmd_list]

    # Join the commands with a horizontal line separator for readability
    cmds = '\n\n———→ '.join(cmd_list)
    embed = discord.Embed(
        title = f"Command List",
        description = f"```———→ {cmds}```",
        color = discord.Color.blue()
    )

    await message.channel.send(embed=embed)