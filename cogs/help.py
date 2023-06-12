import re
import discord
from discord.ext import commands
from utils.config import prefix


class CustomHelpCommand(commands.DefaultHelpCommand):

    # Help command without any arguments
    async def send_bot_help(self, mapping):
        help_text = "Commands:\n"

        # Iterate over each cog in the mapping
        for cog in mapping:
            if cog is not None:
                cog_help = ""
                for command in mapping[cog]:
                    # Get the arguments of the command
                    signature = command.signature
                    signature = signature.split(" ")
                    # Format the arguments
                    text_signature = ""
                    for s in signature:
                        # Remove the brackets
                        for i in [("[", "<"), ("]", ">")]:
                            s = s.replace(i[0], i[1])

                        # Remove the default values
                        pattern = re.escape("=") + "(.*?)" + re.escape(">")
                        s = re.sub(pattern, ">", s)

                        text_signature += " "+s
                    text_signature = text_signature.strip()
                    text_signature = text_signature.replace("  ", " ")
                    # Format the help text
                    if len(mapping[cog]) <= 1:
                        command_info = f"<>{prefix[0]}{command.name} {text_signature} {'―'*(24-len(command.name)-len(text_signature))} {command.short_doc}<>"
                    else:
                        command_info = f"{prefix[0]}{command.name} {text_signature} {'―'*(24-len(command.name)-len(text_signature))} {command.short_doc}\n"
                    cog_help += command_info
                if cog_help:
                    help_text += f"{cog_help}\n"

        # Split the help text into segments and sort them by segment length
        # Commands from the same cogs will stay grouped as is
        # but single command cogs will be grouped together
        segments = help_text.split("<>")
        segments.sort(key=len)

        # Rejoin the messages and remove extra new lines
        message = "\n".join(segments)
        message = message.replace("\n\n\n", "\n")

        # Format the message
        final_message = []
        message = message.split("\n\n")

        # Iterate over the message segments in reverse order
        for i in range(1, len(message))[::-1]:
            # Add the music cog commands to the top
            if "play a song from youtube" in message[i]:
                final_message.append(message[i])
            elif "Commands:" in message[i]:
                continue
            # Sort the commands within the segments and add them
            else:
                final_message.append("\n".join(sorted(message[i].split("\n"))))
        final_message = "\n\n".join(final_message)

        # Wrap the message in a code block and send as segments to avoid the 2000 character limit
        parts = final_message.split("\n\n")
        await self.get_destination().send(f"# Commands")
        for part in parts:
            if len(part) > 10:
                await self.get_destination().send(f"```yaml\n{part}```".replace("  ", " ―"))

    # Help command with arguments
    async def send_command_help(self, command):
        # Get the aliases of the command
        aliases = command.aliases.copy()
        aliases.insert(0, command.name)

        # Get the help text of the command
        text = f""
        text += f"{command.help}\n"

        # Format it depending on if there are aliases or not
        if len(aliases) == 1:
            text_alias = aliases[0]
        else:
            text_alias = f"{f' | {prefix[0]}'.join(aliases)}"

        # Get the arguments of the command
        signature = command.signature
        signature = signature.split(" ")

        # Format the arguments
        text_signature = ""
        for s in signature:
            for i in [("=None", ""), ("=False", ""), ("=True", ""), ("[", "<"), ("]", ">"), ("=-1", "")]:
                s = s.replace(i[0], i[1])
            text_signature += " "+s

        # Combine the segments and send an embed
        text += f"```yaml\n{prefix[0]}{text_alias} {text_signature}```"

        embed = discord.Embed(title=f"{command.name}", description=f"{text}")
        await self.get_destination().send(embed=embed)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.help_command = CustomHelpCommand()
        bot.help_command.cog = self


async def setup(bot):
    await bot.add_cog(Help(bot))