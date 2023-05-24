import discord
import glob

description = """This prompt."""

async def main(message):
    # Find all module files in the 'modules' folder
    modules = glob.glob("modules\*.py")
    commands = [module[:-3] for module in modules]

     # Iterate over each command
    cmd_list = []
    for command in commands:
        # Replace backslashes with dots to create module name
        module = command.replace("\\", ".")
        # Add the description of the command from the module
        command += "\n"+getattr(__import__(module, fromlist=['']), "description")
        cmd_list.append(command)
    
    # Remove the 'modules\' prefix from the commands
    cmd_list = [i.replace("modules\\", "") for i in cmd_list]

    # Join the commands with a horizontal line separator
    cmds = '\n\n———→ '.join(cmd_list)
    embed = discord.Embed(
        title = f"Command List",
        description = f"```———→ {cmds}```",
        color = discord.Color.blue()
    )

    await message.channel.send(embed=embed)