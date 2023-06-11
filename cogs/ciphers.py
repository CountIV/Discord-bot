import discord
from discord.ext import commands
import base64

class Ciphers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def caesar(self, ctx, *, message):
        """Applies the Caesar cipher to the message."""
        
        ciphered_message = ""

        # Iterate through the given message and get the ASCII value
        for letter in message:
            ascii_val = ord(letter)
            # Check the case of the character and apply the relevant shift
            if letter.isupper() and ascii_val >= 65 and ascii_val <= 90:
                ciphered_letter = chr((ascii_val - 65 - 3) % 26 + 65)
            elif letter.islower() and ascii_val >= 97 and ascii_val <= 122:
                ciphered_letter = chr((ascii_val - 97 - 3) % 26 + 97)
            # If the letter is not a letter of the alphabet, leave it unchanged
            else:
                ciphered_letter = letter
            
            # Append the ciphered letter to the ciphered message
            ciphered_message += ciphered_letter
        
        await ctx.send(ciphered_message)


    @commands.command()
    async def braille(self, ctx, *, message):
        """Converts the given message to Braille."""

        # Dict map of letters and numbers to their braille representation
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

        # Convert the message into braille according to the braille map
        for char in message.upper():
            if char in braille_map:
                braille_message += braille_map[char]
            else:
                braille_message += char
        
        embed = discord.Embed(description=f"{braille_message}")
        await ctx.send(embed=embed)


    @commands.command()
    async def morse(self, ctx, *, message):
        """Converts the given message to Morse code and vice versa."""
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


    @commands.command()
    async def binary(self, ctx, message):
        """Converts the given message to binary and vice versa."""
        binary_message = ""
        # checks if the given message is binary or not
        if True in [True if s in ["0", "1"] else False for s in message]:
            # Binary to alphanumeric
            message = message.strip().split(" ")
            for char in message:
                binary_message += chr(int(char, 2))
        else:
            # Alphanumeric to binary
            for char in message:
                binary_message += f"{ord(char):08b} "
            binary_message = binary_message.strip()

        embed = discord.Embed(description=f"{binary_message}")
        await ctx.send(embed=embed)


    # Encodes messages to and from base64 using subcommands
    @commands.group(aliases=["base64"])
    async def base(self, ctx):
        """Performs encoding or decoding of messages using base64."""
        if ctx.invoked_subcommand is None:
            print("base: no parameters")


    @base.command(aliases=["e"])
    async def encode(self, ctx, *, message):
        """ - base64 encode"""
        response = base64.b64encode(message.encode("utf-8")).decode("utf-8")
        await ctx.send(response)
    

    @base.command(aliases=["d"])
    async def decode(self, ctx, *, message):
        """ - based64 decode"""
        response = base64.b64decode(message).decode("utf-8")
        await ctx.send(response)



async def setup(bot):
    await bot.add_cog(Ciphers(bot))