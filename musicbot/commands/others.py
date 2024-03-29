import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from config import config
import time
from discord import embeds
from discord import message
import time
import psutil
import TenGiphPy
import wikipedia

class Others(commands.Cog):
    """A collection of commands that are not music related
    
    
            Attributes:
            bot: The instance of the bot that is executing the commands"""

    def __init__(self, bot):
        self.bot=bot

    #commands
    @commands.command(name="source", description="View source code", help="-source to view")
    async def _source(self, ctx):
        print("source code")
        await ctx.channel.send("Source code is on github! https://github.com/nuggetcatsoftware/Alpaca-bot")

    @commands.command(name="gifs", description="Grabs you gifs", help="-gifs (target) to grab your gifs")
    async def _gifs(self, ctx, *,giftag:str):
        t = TenGiphPy.Tenor(token="QKTF66N1775V")
        getgifurl = t.random(str(giftag))
        await ctx.send(getgifurl)
    @_gifs.error
    async def tenor_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('what gif you want dude?')
        else:
            raise error
    @commands.command(name="weather", description="Provides weather stats of your city", help="-weather (city) to know the weather")
    async def _weather(self, ctx, *, city: str):
        print(city)
        # Python program to find current 
        # weather details of any city
        # using openweathermap api
        # import required modules
        import requests, json
        # Enter your API key here
        api_key = "599697465b8997b41ed0b72b66702336"
        
        # base_url variable to store url
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        
        city_name = city
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        
        # json method of response object 
        # convert json format data into
        # python format data
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature= current_temperature-273.15
            current_pressure = y["pressure"]
            current_humidiy = y["humidity"]
        
            # store the value of "weather"
            # key in variable z
            z = x["weather"]
        
            # store the value corresponding 
            # to the "description" key at 
            # the 0th index of z
            weather_description = z[0]["description"]
        
            # print following values
            await ctx.send(" Temperature (Celcius) = " +
                            str(current_temperature) + 
                "\n atmospheric pressure (in hPa unit) = " +
                            str(current_pressure) +
                "\n humidity (in percentage) = " +
                            str(current_humidiy) +
                "\n description = " +
                            str(weather_description))
        
        else:
            await ctx.send(" City Not Found ")
    
    @commands.command(name="ball",description="Make life decisions with 8ball!!", help="-ball (your question), to generate wisdom")
    async def _ball(self,ctx, *, query:str):
        ballresponse=[
            "No",
            "yes",
            "concentrate and try again",
            "not likely",
            "Likely",
            "That's not gonna happen"
        ]
        print(query)
        import random
        response=random.choice(ballresponse)
        await ctx.send(response)

    @commands.command(name="urban", description="Search urban dictionary", help="-urban (word) (definition no.) to search your word. NSFW BE WARNED")
    async def _urban(self,ctx,*,query,count=1):
        try:
            count = int(count)
            import requests
            from bs4 import BeautifulSoup
            r = requests.get("http://www.urbandictionary.com/define.php?term={}".format(query))
            soup = BeautifulSoup(r.content, features="html.parser")
            item_id = int(count)
            entries = soup.find_all("div", class_="meaning")
            if item_id == 1:
                item_id -= 1
            if item_id < len (entries):
                await ctx.send("Here is your definition on "+ query)
                await ctx.send(entries[item_id].text)
            else:
                await ctx.send("No result.")
        except ValueError:
            count=1
            import requests
            from bs4 import BeautifulSoup
            r = requests.get("http://www.urbandictionary.com/define.php?term={}".format(query))
            soup = BeautifulSoup(r.content, features="html.parser")
            item_id = int(count)
            entries = soup.find_all("div", class_="meaning")
            if item_id == 1:
                item_id -= 1
            if item_id < len (entries):
                await ctx.send("Here is your definition on "+ query)
                await ctx.send(entries[item_id].text)
            else:
                await ctx.send("No result.")
    
    @commands.command(name="hourly", description="Get your hourly dose of alpaca", help="Just run the command dumbo")
    async def _hourly(self,ctx):
        giftag="alpaca"
        t = TenGiphPy.Tenor(token="QKTF66N1775V")
        getgifurl = t.random(str(giftag))
        await ctx.send(f'{getgifurl}')

    @commands.command(name='ping', description=config.HELP_PING_LONG, help=config.HELP_PING_SHORT)
    async def _ping(self, ctx):
        before = time.monotonic()
        message = await ctx.send("Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong!  `{int(ping)}ms`")
    

    @commands.command(name="wikipedia", description="wikipedia the keyword", help= "-wikipedia (keyword)")
    async def _wikipedia(self, ctx, *, query):
        print(query)
        results = wikipedia.summary(query, sentences=3)
        await ctx.send(results)
    @commands.command(name="Debug", description="For nerds only", help="don't even try this ")
    async def _debug(self, ctx):
        print("Debug command")
        await ctx.send("IF you are reading this: The bot has: \n 0: Exceptions raised \n Unknown number of warnings \n Bot is online")
        time.sleep(1)
        await ctx.send("Host clinet ram usage: ")
        await ctx.send(psutil.virtual_memory())
        before = time.monotonic()
        message = await ctx.send("Ping: ")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Ping:  `{int(ping)}ms`")

    @commands.command(name="issues", description="Report issues with this command", help="-issue for further instructions")
    async def _issues(self,ctx):
        print("issue command issued! YOU HAVE A BUG DIPSHIT, FIX IT")
        embedVar = discord.Embed(title="Issues", description="Please see below are ways to tech support or bug report.Sorry for any inconvenience.", color=0xffd700)
        embedVar.add_field(name="Discord", value="Go to the tech support and we will have developers to help you. Click [here](https://discord.gg/KggWRtC7Z9)", inline=False)
        embedVar.add_field(name="Github", value="Report serious bugs to devs. ONLY USE IT FOR BUGS. Tech support will not be addressed!! Click [here](https://github.com/nuggetcatsoftware/Alpaca-bot/issues)", inline=False)
        embedVar.add_field(name="Fix it yourself", value="Click [here](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline=False)
        await ctx.channel.send(embed=embedVar)
    @commands.command(name="query", description="Checks server query", help="-query checks the server where you sent your command.")
    async def _query(self, ctx):
        owner=str(ctx.guild.owner)
        region = str(ctx.guild.region)
        guild_id = str(ctx.guild.id)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)
        desc=ctx.guild.description
        
        embed = discord.Embed(
            title=ctx.guild.name + " Server Information",
            description=desc,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=guild_id, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)

        await ctx.send(embed=embed)

        members=[]
        async for member in ctx.guild.fetch_members(limit=150) :
            await ctx.send('Name : {}\t Status : {}\n Joined at {}'.format(member.display_name,str(member.status),str(member.joined_at)))

def setup(bot):
    bot.add_cog(Others(bot))