import discord,json,requests
from discord.ext import commands

class nature(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Module {} is loaded'.format(self.__class__.__name__))
    
    @commands.command()
    async def cat(self, ctx):
        for item in  json.loads(requests.get("https://api.thecatapi.com/v1/images/search").text):
            embed = discord.Embed(color = discord.Color.blue())
            embed.set_image(url = item["url"])
            return await ctx.send(embed=embed)
    @commands.command()
    async def dog(self,ctx):
        response = requests.get('https://api.thedogapi.com/v1/images/search')
        json_data = json.loads(response.text)
        url = json_data[0]['url']

        embed = discord.Embed(title ="Вот собачка! Гаф!",color = 0xff9900)
        embed.set_image( url = url )

        await ctx.send( embed = embed )
 
    @commands.command()
    async def panda(self, ctx):
        response = requests.get('https://some-random-api.ml/img/panda')
        jsoninf = json.loads(response.text)
        url = jsoninf['link']
        embed = discord.Embed(color = 0xff9900)
        embed.set_image(url = url)
        await ctx.send(embed = embed)

    @commands.command()
    async def bird(self, ctx):
        response = requests.get('https://some-random-api.ml/img/birb')
        jsoninf = json.loads(response.text)
        url = jsoninf['link']    
        embed = discord.Embed(color = 0xff9900)
        embed.set_image(url = url)
        await ctx.send(embed = embed)

    @commands.command()
    async def fox(self, ctx):
        response = requests.get('https://some-random-api.ml/img/fox')
        jsoninf = json.loads(response.text)
        url = jsoninf['link']    
        embed = discord.Embed(color = 0xff9900)
        embed.set_image(url = url)
        await ctx.send(embed = embed)

    @commands.command()
    async def koala(self, ctx):
        response = requests.get('https://some-random-api.ml/img/koala')
        jsoninf = json.loads(response.text)
        url = jsoninf['link']    
        embed = discord.Embed(color = 0xff9900)
        embed.set_image(url = url)
        await ctx.send(embed = embed)
    @commands.command()
    async def red_panda(self, ctx):
        response = requests.get('https://some-random-api.ml/img/red_panda')
        jsoninf = json.loads(response.text)
        url = jsoninf['link']    
        embed = discord.Embed(color = 0xff9900)
        embed.set_image(url = url)
        await ctx.send(embed = embed)

    @commands.command()
    async def meme(self, ctx):
        response = requests.get('https://some-random-api.ml/meme')
        jsoninf = json.loads(response.text)
        url = jsoninf['link']    
        embed = discord.Embed(color = 0xff9900)
        embed.set_image(url = url)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(nature(bot))