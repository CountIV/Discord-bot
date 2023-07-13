import discord
from discord.ext import commands
import requests
from datetime import datetime
import json

class Lol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = open(".env/riot_api_key", "r").read()

    @commands.command()
    async def clash(self, ctx):
        """Provides information on the start time of the next clash event."""
        # API configuration
        api_url = "https://euw1.api.riotgames.com/lol/clash/v1/tournaments" + "?api_key=" + self.api_key

        # Response body gets saved in data variable
        response = requests.get(api_url)
        data = response.json()

        # If no to data is sent back
        if data == []:
            await ctx.send("No upcoming Clash found, stay tuned!")
            return

        # Get the smallest, which also means the nearest clash, start and end date
        min_start_time = float("inf")
        min_end_time = float("inf")
        for item in data:
            start_time = item['schedule'][0]['registrationTime']
            end_time = item['schedule'][0]['startTime'] # Yes, startTime is actually ending time

            if start_time < min_start_time:
                min_start_time = start_time
                min_end_time = end_time

        # TierIV starts at start_time, every other tier later in a time not present in data
        # TODO: Implement the other tiers and don't hardcode it in the code
        tierIII_adjustment = 8100000 # 2h15m

        # Get datetime objects
        clash_start_time = datetime.fromtimestamp((min_start_time + tierIII_adjustment) / 1000)
        clash_end_time = datetime.fromtimestamp(min_end_time / 1000)
        current_time = datetime.now()
        time_until_clash_start = clash_start_time - current_time

        # Respond with appropriate message depending on the current time
        bot_response = None
        if clash_end_time < current_time:
            bot_response = "Registration has ended, may your Clash be victorious!"
        elif clash_start_time < current_time:
            bot_response = "Clash is open right now, @everyone all aboard!"
        else:
            days = time_until_clash_start.days
            hours = time_until_clash_start.seconds // 3600
            minutes = (time_until_clash_start.seconds // 60) % 60
            seconds = time_until_clash_start.seconds % 60
            bot_response = f"Next Clash starts in {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

        await ctx.send(bot_response)

    @commands.command()
    async def lol(self, ctx, *, username):
        """Search League player stats by username"""
        view = LeagueProfile(username, self.api_key)
        embed = view.front_page()

        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Lol(bot))


# This handles displaying embed and navigation buttons
class LeagueProfile(discord.ui.View):
    def __init__(self, username, api_key):
        super().__init__()

        api_url_summoner = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}?api_key={api_key}"
        self.summoner_data = requests.get(api_url_summoner).json()
        self.name = self.summoner_data['name']
        encryptedSummonerId = self.summoner_data["id"]

        api_url_ranked = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{encryptedSummonerId}?api_key={api_key}"
        self.ranked_data = requests.get(api_url_ranked).json()

        api_url_mastery = f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{encryptedSummonerId}?api_key={api_key}"
        self.mastery = requests.get(api_url_mastery).json()

    # Creates embed for initial page, returns Discord embed
    def front_page(self):
        # Checks last activity in League client
        # Probably updated every time a game in LoL or TFT ends
        date = datetime.fromtimestamp(self.summoner_data['revisionDate'] // 1000).strftime("%Y-%m-%d %H:%M")

        # Build embed with returned data
        embed = discord.Embed(title=f"{self.name}", color=discord.Color.blue())
        if self.ranked_data != []:
            rank = f"{self.ranked_data[0]['tier']} {self.ranked_data[0]['rank']}"
            wins = self.ranked_data[0]['wins']
            losses = self.ranked_data[0]['losses']
            winrate = round(wins / (wins + losses) * 100, 1)

            embed.add_field(name="Rank", value=rank, inline=False)
            embed.add_field(name="Wins", value=wins)
            embed.add_field(name="Losses", value=losses)
            embed.add_field(name="Winrate", value=f"{winrate}%")
        else:
            embed.add_field(name="Rank", value="UNRANKED", inline=False)
        embed.add_field(name="Last seen", value=date)

        return embed

    # Creates embed for initial page, returns Discord embed
    def mastery_page(self):
        # champions.json has champion names
        with open("resources/champions.json", encoding="UTF-8") as file:
            champion_data = json.load(file)

        # Build Embed
        embed = discord.Embed(title=f"{self.name}: Mastery", color=discord.Color.blue())
        for index, champion in enumerate(self.mastery):
            # Get champion's name from using champion's id
            champion_name = champion_data[str(champion["championId"])]
            # Get champion's mastery points
            champion_mastery_points = champion["championPoints"]
            embed.add_field(name=f"{index+1}. {champion_name}", value=f"{champion_mastery_points} points")
            
            # End for loop with typed amount of entries
            if index == 8:
                break

        return embed


    # Left Button
    @discord.ui.button(label="Front Page", style=discord.ButtonStyle.blurple)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.front_page()
        await interaction.response.edit_message(embed=embed)

    # Right Button
    @discord.ui.button(label="Mastery", style=discord.ButtonStyle.blurple)
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.mastery_page()
        await interaction.response.edit_message(embed=embed)