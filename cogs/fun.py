import discord
from discord.ext import commands
import nekos
import datetime

class fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Module {} is loaded'.format(self.__class__.__name__))



    @commands.command() # Декоратор команды
    async def kiss(self, ctx, member : discord.Member): # Название команды и аргумент
        if member == ctx.message.author: # Проверка кого упомянули
            await ctx.send('Вы не можете поцеловать сами себя.')
        else:
            emb = discord.Embed(description= f'{member.mention}, Вас поцеловал(а) {ctx.message.author.mention}.') # Переменная ембеда и описание
            emb.set_image(url=nekos.img('kiss')) # Ищем картинку и ставим её в ембед

            await ctx.send(embed=emb) # Отпрвака ембед

            
    @commands.command() # Декоратор команды
    async def hug(self, ctx, member : discord.Member): # Название команды и аргумент
        if member == ctx.message.author: # Проверка кого упомянули
            await ctx.send('Вы не можете обнять сами себя.')
        else:
            emb = discord.Embed(description= f'{member.mention}, Вас обнял(а) {ctx.message.author.mention}.') # Переменная ембеда и описание
            emb.set_image(url=nekos.img('hug')) # Ищем картинку и ставим её в ембед

            await ctx.send(embed=emb) # Отпрвака ембед

            
    @commands.command() # Декоратор команды
    async def slap(self, ctx, member : discord.Member): # Название команды и аргумент
        if member == ctx.message.author: # Проверка кого упомянули
            await ctx.send('Вы не можете ударить сами себя.')
        else:
            emb = discord.Embed(description= f'{member.mention}, Вас ударил(а) {ctx.message.author.mention}.') # Переменная ембеда и описание
            emb.set_image(url=nekos.img('slap')) # Ищем картинку и ставим её в ембед

            await ctx.send(embed=emb) # Отпрвака ембед

            
    @commands.command() # Декоратор команды
    async def pat(self, ctx, member : discord.Member): # Название команды и аргумент
        if member == ctx.message.author: # Проверка кого упомянули
            await ctx.send('Вы не можете погладить сами себя.')
        else:
            emb = discord.Embed(description= f'{member.mention}, Вас погладил(а) {ctx.message.author.mention}.') # Переменная ембеда и описание
            emb.set_image(url=nekos.img('pat')) # Ищем картинку и ставим её в ембед

            await ctx.send(embed=emb) # Отпрвака ембед

@commands.command() # Декоратор команды
async def profile(self,ctx, userf: discord.Member = None): # Название команды и аргумент
        user = ctx.message.author if userf == None else userf # Проверка указан ли пользователь, если нет то заменяем автором команды
        status = user.status # Получаем статус

        if user.is_on_mobile() == True: stat = 'На телефоне' # Проверка статуса и указываем статус
        if status == discord.Status.online: stat = 'В сети' # Проверка статуса и указываем статус
        elif status == discord.Status.offline: stat = 'Не в сети' # Проверка статуса и указываем статус
        elif status == discord.Status.idle: stat = 'Не активен' # Проверка статуса и указываем статус
        elif status == discord.Status.dnd: stat = 'Не беспокоить' # Проверка статуса и указываем статус

        create_time = (datetime.datetime.today()-user.created_at).days # Узнаем кол-во дней в дискорде
        join_time = (datetime.datetime.today()-user.joined_at).days # Узнаем кол-во дней на сервере
        emb = discord.Embed(title='Профиль', colour= user.color) # Делаем ембед и устанавливаем цвет
        emb.add_field(name= 'Имя/Ник', value= f"{user.name}/{user.display_name}({user.id})", inline= False) # Добавляем поле и заполняем 
        emb.add_field(name= 'Статус', value= stat, inline= False)
        activ = ""
        for i in user.activities:
            if i.type == discord.ActivityType.custom:
                activ += f":{i.emoji.name}:{i.name}\n"
            if i.type == discord.ActivityType.playing:
                activ += f"Играет в`{i.name}`\n"
            if i.type == discord.ActivityType.listening:
                title = i.title
                name = i.name
                artist = ""
                for i in i.artists:
                    artist += f"{i}|"
                activ += f"Слушает `{title}` от`{artist}` в `{name}`\n"

        emb.add_field(name="Активности",value=activ,inline=False)
        
        if create_time == 0: # Проверка на число дней
            emb.add_field(name= 'Присоиденился к дискорду', value= f'{user.created_at.strftime("%d.%m.%Y")} ( Меньше дня )', inline= False) # Добавляем поле и заполняем дни в дискорде
        else:
            emb.add_field(name= 'Присоиденился к дискорду', value= f'{user.created_at.strftime("%d.%m.%Y")} ( {create_time} {postfix(create_time, "день", "дня", "дней")})', inline= False)# Добавляем поле и заполняем кол-во дней в дискорде и подбираем окончание
        if join_time == 0: # Проверка на число дней
            emb.add_field(name= 'Присоединился к серверу', value= f'{user.joined_at.strftime("%d.%m.%Y")} ( Меньше дня )', inline= False) # Добавляем поле и заполняем дни на сервере
        else:
            emb.add_field(name= 'Присоединился к серверу', value= f'{user.joined_at.strftime("%d.%m.%Y")} ( {join_time} {postfix(join_time, "день", "дня", "дней")} )', inline= False) # Добавляем поле и заполняем кол-во дней на сервере и подбираем окончание
        emb.add_field(name= 'Наивысшая роль', value= f"<@&{user.top_role.id}>", inline= False) # Добавляем поле и заполняем роль
        emb.set_thumbnail(url= user.avatar_url) # Устанавливаем картинку сбоку ( В душе хз как назвать xD )

        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(fun(bot))
