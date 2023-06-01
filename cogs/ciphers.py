import discord
from discord.ext import commands

class Ciphers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def caesar(self, ctx, *, message):
        """ - Applies Ceasar cipher to the message """
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


    @commands.command()
    async def braille(self, ctx, *, message):
        """- Converts given message to braille"""
        braille_map = {
            'A': '⠁',   'B': '⠃',   'C': '⠉', 
            'D': '⠙',   'E': '⠑',   'F': '⠋', 
            'G': '⠛',   'H': '⠓',   'I': '⠊', 
            'J': '⠚',   'K': '⠅',   'L': '⠇', 
            'M': '⠍',   'N': '⠝',   'O': '⠕', 
            'P': '⠏',   'Q': '⠟',   'R': '⠗', 
            'S': '⠎',   'T': '⠞',   'U': '⠥', 
            'V': '⠧',   'W': '⠺',   'X': '⠭', 
            'Y': '⠽',   'Z': '⠵',   '0': '⠚', 
            '1': '⠁',   '2': '⠃',   '3': '⠉', 
            '4': '⠙',   '5': '⠑',   '6': '⠋', 
            '7': '⠛',   '8': '⠓',   '9': '⠊',
        }

        braille_message = ""
        for char in message.upper():
            if char in braille_map:
                braille_message += braille_map[char]
            else:
                braille_message += char
        
        embed = discord.Embed(description=f"{braille_message}")
        await ctx.send(embed=embed)
    


    @commands.command()
    async def morse(self, ctx, *, message):
        """- Converts given message to morse code and vice-versa"""
        morse_map = {
        'A': '.-',      'B': '-...',    'C': '-.-.', 
        'D': '-..',     'E': '.',       'F': '..-.', 
        'G': '--.',     'H': '....',    'I': '..', 
        'J': '.---',    'K': '-.-',     'L': '.-..', 
        'M': '--',      'N': '-.',      'O': '---', 
        'P': '.--.',    'Q': '--.-',    'R': '.-.', 
        'S': '...',     'T': '-',       'U': '..-', 
        'V': '...-',    'W': '.--',     'X': '-..-', 
        'Y': '-.--',    'Z': '--..',    '0': '-----', 
        '1': '.----',   '2': '..---',   '3': '...--', 
        '4': '....-',   '5': '.....',   '6': '-....', 
        '7': '--...',   '8': '---..',   '9': '----.'
        }

        alphanumerics = list(morse_map.keys())

        # checks if the given message is morse or not
        if True in [True if s.upper() in alphanumerics else False for s in message] and "/" not in message:
            # Alphanumeric to morse
            message = message.replace(".", " ")
            message = message.replace("-", " ")
            converted = ""
            for char in message.upper():
                if char in morse_map:
                    converted += f"{morse_map[char]} "
                elif char == " ":
                    converted += "/ "
                else:
                    converted += char
            
            # Retain server specific emojis
            if "<:" in converted and ">" in converted:
                old = message.split(" ")
                new = converted.replace(" <:", " / <:")
                new = new.replace("/ /", "/ ")
                new = new.split("/ ")
                for i, seg in enumerate(new):
                    if "<:" in seg:
                        new[i] = old[i]
                converted = "/ ".join(new)
        else:
            # Morse to alphanumeric
            # flips the morse map
            morse_map = {value: key for key, value in morse_map.items()}
            # partition the message
            morse = message.strip().split(" ")
            converted = ''
            for char in morse:
                if char in morse_map:
                    converted += morse_map[char]
                elif char == "/":
                    converted += " "
                else:
                    converted += char

        embed = discord.Embed(description=f"{converted}")
        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Ciphers(bot))