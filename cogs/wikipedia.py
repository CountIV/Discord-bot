import discord
import requests
from discord.ext import commands


class Wikipedia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def wiki(self, ctx, *, search_query):
        """- Searches wikipedia for the given search_query"""
        api = "https://en.wikipedia.org/w/api.php"

        # List of words that are usually not capitalized in titles
        exceptions = ['a', 'an', 'the', 
                      'and', 'but', 'or', 'nor', 'for', 'so', 'yet', 
                      'at', 'by', 'for', 'from', 'in', 'into', 'of', 'off', 'on', 'onto', 'out', 'over', 'to', 'up', 'with'
                      ]
        
        # Reformatting the search query to improve results
        search_query = search_query.split(" ")
        search_query = [s.capitalize() if s not in exceptions else s for s in search_query]
        search_query[0] = search_query[0].capitalize()
        search_query = " ".join(search_query)

        # Parameters for the wikipedia api
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