import discord
import requests
from discord.ext import commands
from utils.config import wikipedia_api


class Wikipedia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def wiki(self, ctx, *, search_query):
        """- Searches wikipedia for the given search_query"""
        api = wikipedia_api

        params = {
            "action": "query",
            "format": "json",
            "prop": "info|extracts",
            "inprop": "url",
            "exintro": "",
            "explaintext": "",
            "titles": search_query
        }

        try:
            # Send the API request
            response = requests.get(api, params=params).json()
            page_id = list(response['query']['pages'].keys())[0]
            page_data = response['query']['pages'][page_id]

            if page_id != "-1":
                # Get the page title, summary, and URL
                title = page_data['title']
                summary = page_data['extract']
                url = page_data['fullurl']

                # Truncate the summary if it exceeds the maximum length
                if len(summary) > 1900:
                    summary = summary[:1897] + "..."

                # Format and send the response
                response = f"**{title}**\n{summary}\n\nRead more: {url}"
                await ctx.send(response)
            else:
                # If the search query does not match any page, display an error
                await ctx.send("No Wikipedia page found for the given query.")
        except KeyError:
            # If the API response is not as expected, display an error
            await ctx.send("An error occurred while retrieving the Wikipedia page.")


async def setup(bot):
    await bot.add_cog(Wikipedia(bot))