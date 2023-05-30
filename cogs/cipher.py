import discord
from discord.ext import commands

class Cipher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='- Applies Ceasar cipher to the message')
    async def cipher(self, ctx, *, message):
        # Ciphers one letter at time
        ciphered_message = ""
        for letter in message:
            ascii_val = ord(letter)
            if letter.isupper() and ascii_val >= 65 and ascii_val <= 90:
                ciphered_letter = chr((ascii_val - 65 - 3) % 26 + 65)                
            elif letter.islower() and ascii_val >= 97 and ascii_val <= 122:
                ciphered_letter = chr((ascii_val - 97 - 3) % 26 + 97)
            else:
                ciphered_letter = letter
            ciphered_message += ciphered_letter
        
        await ctx.send(ciphered_message)            



async def setup(bot):
    await bot.add_cog(Cipher(bot))