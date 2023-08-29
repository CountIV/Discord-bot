import discord
from discord.ext import commands
import requests
from datetime import datetime
import json

# Get riot api key from .env folder
api_key = open(".env/riot_api_key", "r").read()

class Lol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clash(self, ctx):
        """Provides information on the start time of the next clash event."""
        # API configuration
        api_url = "https://euw1.api.riotgames.com/lol/clash/v1/tournaments" + "?api_key=" + api_key

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
        view = LeagueProfile(username)
        embed = view.front_page()

        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Lol(bot))


# This class handles displaying and editing embeds and navigation buttons
class LeagueProfile(discord.ui.View):
    # username is input provided by discord user
    def __init__(self, username):
        super().__init__()

        # Use summoner name to fetch data related that summoner
        api_url_summoner = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}?api_key={api_key}"
        self.summoner_data = requests.get(api_url_summoner).json()
        self.name = self.summoner_data['name']
        encryptedSummonerId = self.summoner_data["id"]
        self.puuid = self.summoner_data["puuid"]

        # Fetch summoner ranked data
        api_url_ranked = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{encryptedSummonerId}?api_key={api_key}"
        self.ranked_data = requests.get(api_url_ranked).json()

        # Fetch summoner mastery data
        api_url_mastery = f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{encryptedSummonerId}?api_key={api_key}"
        self.mastery = requests.get(api_url_mastery).json()

        # Fetch summoner match history data
        api_url_match_history = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.puuid}/ids?start=0&count=100&api_key={api_key}"
        self.match_history = requests.get(api_url_match_history).json()

        # Track which match history index match_fetch should fetch
        self.match_index = 0

    # Fetch summoner's match data
    def match_fetch(self):
        match_id = self.match_history[self.match_index]
        api_url_match = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
        return requests.get(api_url_match).json()

    # Creates embed for initial page, returns Discord embed
    def front_page(self):
        # Checks last activity in League client
        # Probably updated every time a game in LoL or TFT ends
        date = datetime.fromtimestamp(self.summoner_data['revisionDate'] // 1000).strftime("%Y-%m-%d %H:%M")

        # Build embed
        embed = discord.Embed(title=f"{self.name}", color=discord.Color.blue())
        for ranked_mode in self.ranked_data:
            if ranked_mode["queueType"] == "RANKED_SOLO_5x5":
                rank = f"{ranked_mode['tier']} {ranked_mode['rank']}"
                wins = ranked_mode['wins']
                losses = ranked_mode['losses']
                winrate = round(wins / (wins + losses) * 100, 1)

                embed.add_field(name="Rank", value=rank, inline=False)
                embed.add_field(name="Wins", value=wins)
                embed.add_field(name="Losses", value=losses)
                embed.add_field(name="Winrate", value=f"{winrate}%")
                break
        else:
            embed.add_field(name="Rank", value="UNRANKED", inline=False)
        embed.add_field(name="Last seen", value=date)

        return embed

    # Creates embed for initial page, returns Discord embed
    def mastery_page(self):
        # champions.json has champion names
        with open("resources/champions.json", encoding="UTF-8") as file:
            champion_data = json.load(file)

        # Build embed
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

    # Create embed based on the most recent game data
    def match_page(self):
        # Fetch data from match_fetch()
        match = self.match_fetch()
        participants = match["info"]["participants"]
        # Find player inside participants by matching puuid
        for player in participants:
            if self.puuid == player["puuid"]:
                # This is empty, because player variable is what we want it be when this loop breaks
                break

        # Get relevant data
        champion = player["championName"]
        position = player["teamPosition"]
        role = self.convert_position(position)
        kda = f'{player["kills"]}/{player["deaths"]}/{player["assists"]}'
        result = "Win" if player["win"] else "Loss"

        # Build embed
        embed = discord.Embed(title=f"{self.name}: Game {self.match_index + 1}", color=discord.Color.blue())
        embed.add_field(name="Champion", value=champion)
        embed.add_field(name="Role", value=role)
        embed.add_field(name="KDA", value=kda)
        embed.add_field(name="Result", value=result)

        return embed

    @staticmethod
    def convert_position(position):
        # Convert position using match and return corresponding role
        match position:
            case "TOP":
                role = "TOP"
            case "JUNGLE":
                role = "JNG"
            case "MIDDLE":
                role = "MID"
            case "BOTTOM":
                role = "ADC"
            case "UTILITY":
                role = "SUP"
        return role

    # Button1
    @discord.ui.button(label="Front Page", style=discord.ButtonStyle.blurple)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.front_page()
        await interaction.response.edit_message(embed=embed)

    # Button2
    @discord.ui.button(label="Games", style=discord.ButtonStyle.blurple)
    async def button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.match_page()
        await interaction.response.edit_message(embed=embed)

    # Button3
    @discord.ui.button(label="Mastery", style=discord.ButtonStyle.blurple)
    async def button3(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.mastery_page()
        await interaction.response.edit_message(embed=embed)

    # Button4
    @discord.ui.button(label="🔼", style=discord.ButtonStyle.blurple)
    async def button4(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.match_index != 0:
            self.match_index -= 1
            embed = self.match_page()
            await interaction.response.edit_message(embed=embed)

    # Button5
    @discord.ui.button(label="🔽", style=discord.ButtonStyle.blurple)
    async def button5(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.match_index += 1
        embed = self.match_page()
        await interaction.response.edit_message(embed=embed)