import discord
from discord.ext import commands
import datetime
import random
import nekos
from discord_components import DiscordComponents, ComponentsBot, Button
import pyowm
import wikipedia
import asyncio
import time
import COVID19Py
import json
import os
import sqlite3
import wavelink

bot = commands.Bot(command_prefix=">", help_command=None, intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Бот в сети!")
   



    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("Тестинг (мой префикс >)")) # Изменяем статус боту

    """Статус
    Также можно установить не только Game, но и Watching или Streaming..
    Точные классы посмотрите в документации по discord.py
    https://discordpy.readthedocs.io/en/latest/api.html
    """


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    msg = message.content.lower()
    greeting_words = ["hello", "hi", "привет"]
    censored_words = ["дурак", "дура", "придурок"]

    if msg in greeting_words:
        await message.channel.send(f"{message.author.name}, приветствую тебя!")

    # Filter censored words
    for bad_content in msg.split(" "):
        if bad_content in censored_words:
            await message.channel.send(f"{message.author.mention}, ай-ай-ай... Плохо, плохо, так нельзя!")


#@bot.event
#async def on_member_join(member):
    #channel = bot.get_channel() # Передайте ID канала
    #role = discord.utils.get(member.guild.roles, id=role_id) # Передайте ID роли

    #await member.add_roles(role)


@bot.event
async def on_command_error(ctx, error):
    """Работа с ошибками
    
    Работать с ошибками можно с двумя способами, как в видео (11 серия "Работа с ошибками")
    или же в данной функции. Легче всего использовать второй вариант.. 
    """

    print(error)

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author}, у вас недостаточно прав для выполнения данной команды!")
    elif isinstance(error, commands.UserInputError):
        await ctx.send(embed=discord.Embed(
            description=f"Правильное использование команды: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief})\nExample: {ctx.prefix}{ctx.command.usage}"
        ))


@bot.command(name="кик", brief="Выгнать пользователя с сервера", usage="kick <@user> <reason=None>")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete(delay=1) # Если желаете удалять сообщение после отправки с задержкой

    await member.send(f"Ты был кикнут с сервера") # Отправить личное сообщение пользователю
    await ctx.send(f"Участник {member.mention} был кикнут с сервера")
    await member.kick(reason=reason)


@bot.command()
async def help(ctx):
    """Команда help
    Чтобы не писать тысячу строк одинакового кода, лучше занесем название и описание команд в списки,
    и переберм в цикле.
    """

    embed = discord.Embed(
        title="Все команды",
        description="Тут находится все команды бота: (и доп я добавил некоторые команды благодаря Кустик#5555 и благодаря zxcmishoron#8290)"
    )
    commands_list = ["clear", "кик", "бан", "unban", "serverinfo", "avatar", "ping", "мут", "размут", "kiss", "hug", "slap", "pat", "credits(в разработке)", "cat", "dog", "panda", "bird", "fox", "koala", "red_panda", "Мемы",]
    descriptions_for_commands = ["Чистит чат от лишних сообщений", "Кикает участника с сервера", "Банит участника", "Разбанивает участника", "Даёт информацию о сервере", "Показывает аватар пользователя", "Даёт информацию а пинге бота", "Мьютит участника", "Снимает мут с участника", "Целует упомянутого участника которого вы упомяните", "Обнимает упомянутого участника которого вы упомяните", "Ударяет упомянутого участника которого вы упомяните", "Гладит упомянутого участника которого вы упомяните", "Команда времнно не работает", "Показывает рандомную фото любого кота(кошки возможно)", "Показывает рандомную фото любой собаки", "Показывает рандомную фото любой птицы", "Показывает рандомную фото любой коалы", "Показывает рандомную фото любой лисы", "Показывает рандомную фото любой коалы", "Показывает рандомную фото любого малой панда", "Показывает рандомный мем( пишите так >мемы начиная с маленькой буквы)"]

    for command_name, description_command in zip(commands_list, descriptions_for_commands):
        embed.add_field(
            name=command_name,
            value=description_command,
            inline=False # Будет выводиться в столбик, если True - в строчку
        )


    await ctx.author.send(embed=embed)



#@bot.command(name="join", brief="Подключение к голосовому каналу", usage="join")
#async def join_to_channel(ctx):
    #global voice
    #voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    #channel = ctx.message.author.voice.channel

    #if voice and voice.is_connected():
        #await voice.move_to(channel)
    #else:
        #voice = await channel.connect()
        #await ctx.send(f"Bot was connected to the voice channel")


@bot.command(name="leave", brief="Отключение от голосового канала", usage="leave")
async def leave_from_channel(ctx):
    global voice
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.disconnect()
        await ctx.send(f"Bot was connected to the voice channel")

@bot.command(aliases=['av']) # Декоратор команды
async def avatar(ctx, member : discord.Member = None): # Название команды и аргументы
    user = ctx.message.author if member == None else member # Проверка аргуменат и переменная участника
    emb = discord.Embed( # Переменная ембеда
        title=f'Аватар пользователя {user}', # Заполняем заголовок
        description= f'[Ссылка на изображение]({user.avatar_url})', # Запонлняем описание
        color=user.color # Устанавливаем цвет
    )
    emb.set_image(url=user.avatar_url) # Устанавливаем картинку
    await ctx.send(embed=emb) # Отпрвака ембеда 

@bot.command()
async def send_a( ctx ):
    await ctx.author.send( 'Привет!' )

@bot.command() # Декоратор команды
async def ping(ctx): # # Название команды
    emb = discord.Embed( # Переменная ембеда
        title= 'Текущий пинг', # Заполняем заголовок
        description= f'{bot.ws.latency * 1000 :.0f} ms' # Запонлняем описание
    )
    await ctx.send(embed=emb) # Отпрвака ембеда 

@bot.command(aliases=['sc']) # Декоратор команды
async def servercount(ctx): # Название команды
    await ctx.send(f'Бот есть на {len(bot.guilds)} серверах') # Выводит кол-во серверов бота    

@bot.command(aliases=['rt']) # Декоратор команды
async def ran_avatar(ctx): # Название команды
    emb = discord.Embed(description= 'Вот подобраная Вам аватарка.') # Переменная ембеда и его описание
    emb.set_image(url=nekos.img('avatar')) # Тут мы с помощью новой библиотеки ищем картинку на тему аватар и ставим её в ембед
    await ctx.send(embed=emb)  # Отпрвака ембеда 
    
@bot.command(aliases=['rc']) # Декоратор команды
async def ran_color(ctx): # Название команды
    clr = (random.randint(0,16777215)) # Генерируем рандомное число от 0 до 16777215, это нужно чтобы сделать цвет
    emb = discord.Embed( # Переменная ембеда
        description= f'Сгенерированый цвет : ``#{hex(clr)[2:]}``', # Jписание ембеда, и код с помощью которого мы делаем цвет
        colour= clr # Устанавливаем цвет ембеду
    )

    await ctx.send(embed=emb) # Отпрвака ембеда 
    
@bot.command()
async def button(ctx):
    await ctx.send(
        "Hello World!",
        components = [
            Button(label = "WOW button!")
        ]
    )

    interaction = await bot.wait_for("button_click", check = lambda i: i.component.label.startswith("WOW"))
    await interaction.send(content = "Button clicked!")

def random_meme():
    with open('memes_data.txt', 'r') as file:
        memes = file.read().split(',')
    picked_meme = random.choice(memes)
    return picked_meme

@bot.command()
async def мемы(ctx):
    emb = discord.Embed()
    emb.set_image(url= random_meme())
    await ctx.send(embed=emb)    

bot.load_extension("jishaku")


@bot.command() # Попытки 5
@commands.is_owner()
async def угадайка(ctx):
    await ctx.message.delete()
    num = random.randint(1, 20)
    print(num)
    attems = 1
    msg = await ctx.send('Подождите...')
    while attems < 6:
        emb = discord.Embed(
            title = f'Попытка №{attems}',
            description= 'Угадайте число от 1 до 20'
        )
        await msg.edit(content= None, embed=emb)
        
        try:
            msg_o = await  bot.wait_for('message', timeout= 30.0, check= lambda msg_o: msg_o.author == ctx.author)
        except asyncio.TimeoutError:
            await msg.edit(content= 'Время вышло!', embed=None)
            break
        else:
            if num == int(msg_o.content):
                emb1 = discord.Embed(
                    title= 'Вы победили!',
                    description= 'Вы угадали число!'
                )
                await msg_o.delete()
                await msg.edit(content= None, embed=emb1)
                break
            else:
                attems_h = 5 - attems
                attems = attems + 1

                if attems == 6:
                    emb2 = discord.Embed(
                        title= 'Вы проиграли!',
                        description= f'Загаданое число было : {num}'
                    )
                    await msg_o.delete()
                    await msg.edit(embed=emb2)
                    break

                emb2 = discord.Embed(
                    title= 'Неудачная попытка!',
                    description= f'Вы не угадали число у вас осталось {attems_h} попыток'
                )
                await msg.edit(content= None, embed=emb2)
                await msg_o.delete() 
                await asyncio.sleep(5)



@bot.command(aliases=['sr'])
async def serverinfo(ctx):
    members = ctx.guild.members
    online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
    offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
    idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
    dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
    allchannels = len(ctx.guild.channels)
    allvoice = len(ctx.guild.voice_channels)
    alltext = len(ctx.guild.text_channels)
    allroles = len(ctx.guild.roles)
    embed = discord.Embed(title=f"{ctx.guild.name}", color=0xff0000, timestamp=ctx.message.created_at)
    embed.description=(
        f":timer: Сервер создали **{ctx.guild.created_at.strftime('%A, %b %#d %Y')}**\n\n"
        f":flag_white: Регион **{ctx.guild.region}\n\nГлава сервера **{ctx.guild.owner}**\n\n"
        f":tools: Ботов на сервере: **{len([m for m in members if m.bot])}**\n\n"
        f":green_circle: Онлайн: **{online}**\n\n"
        f":black_circle: Оффлайн: **{offline}**\n\n"
        f":yellow_circle: Отошли: **{idle}**\n\n"
        f":red_circle: Не трогать: **{dnd}**\n\n"
        f":shield: Уровень верификации: **{ctx.guild.verification_level}**\n\n"
        f":musical_keyboard: Всего каналов: **{allchannels}**\n\n"
        f":loud_sound: Голосовых каналов: **{allvoice}**\n\n"
        f":keyboard: Текстовых каналов: **{alltext}**\n\n"
        f":briefcase: Всего ролей: **{allroles}**\n\n"
        f":slight_smile: Людей на сервере **{ctx.guild.member_count}\n\n"
    )

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"ID: {ctx.guild.id}")
    embed.set_footer(text=f"ID Пользователя: {ctx.author.id}")
    await ctx.send(embed=embed)  


@bot.event
async def on_message_delete(message):
    channel = bot.get_channel(951626331496521758)
    if message.content is None:
        return;
    embed = discord.Embed(colour=0xff0000, description=f"**{message.author} Удалил сообщение в канале {message.channel}** \n{message.content}",timestamp=message.created_at)

    embed.set_author(name=f"{message.author}", icon_url=f'{message.author.avatar_url}')
    embed.set_footer(text=f'ID Пользователя: {message.author.id} | ID Сообщения: {message.id}')
    await channel.send(embed=embed)
    return            

@bot.event
async def on_message_edit(before, after):
    channel = bot.get_channel(951626331496521758)
    if before.author == Bot.user:
        return
    if before.content is None:
        return;
    elif after.content is None:
        return;
    message_edit = discord.Embed(colour=0xff0000,
                                 description=f"**{before.author} Изменил сообщение в канале {before.channel}** "
                                             f"\nСтарое сообщение:{before.content}"
                                             f"\n\nНовое сообщение: {after.content}",timestamp=before.created_at)

    message_edit.set_author(name=f"{before.author}",icon_url=f"{before.author.avatar_url}")
    message_edit.set_footer(text=f"ID Пользователя: {before.author.id} | ID Сообщения: {before.id}")
    await channel.send(embed=message_edit)
    return

@bot.command()
@commands.is_owner()
async def inv(ctx, channel: discord.abc.GuildChannel):
    try:
        await ctx.message.delete()
    except Exception:
        pass

    log = bot.get_channel(Сюда) #id канала с логами приглашений
    
    invitelink = await channel.create_invite(max_uses=100, max_age=21600, unique=True) #Настраиваем само приглашение - количество использований и длительность действия. Время в секундах

    emb = discord.Embed(
        title= 'Создано приглашение на сервер',
        color= discord.Color.orange()
    )
    emb.add_field(
        name= 'Приглашение создано участником:',
        value = ctx.author.mention
    )

    await ctx.author.send(f'Вы запросили ссылку-приглашение на сервер. Здорово! Теперь отправь eё другу:\n{invitelink}') #приглашение в ЛС пользователю
    await log.send(embed=emb)

@bot.command()
async def rep(ctx,member: discord.Member = None,*,arg = None):

    channel = bot.get_channel(951632124920885290) #Айди канала жалоб

    if member == None:
        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))
        return

    if arg == None:
        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))
        return

    emb = discord.Embed(description =f'**:shield: {ctx.author.mention}, Вы отправили жалобу на пользователя {member.mention}.\n:bookmark_tabs: По причине: {arg}**', color=0x0c0c0c)
    await ctx.send(embed = emb)

    embed = discord.Embed(description =f'**:shield: На пользователя {member.mention} была отправлена жалоба.\n:bookmark_tabs: По причине: {arg}\n:bust_in_silhouette: Автор жалобы: {ctx.author.mention}**', color=0x0c0c0c)
    await channel.send(embed = embed)

@bot.command()
async def covid(ctx, code: str= None):
    covid19 = COVID19Py.COVID19()
    if not code:
        location = covid19.getLocationByCountryCode("RU")[0]
    else:
        code = code.upper()
        with open('country_codes.json') as h_file:
            c_codes = json.load(h_file)
        if not code in c_codes:
            await ctx.send('Неверный код страны.')
            return
        location = covid19.getLocationByCountryCode(code)[0]
    date = location['last_updated'].split("T")
    time = date[1].split(".")

    embed = discord.Embed(
        title = f'Случаи заболевания COVID-19, {location["country"]}:',
        description = f'''Заболевших: {location['latest']['confirmed']}\nСмертей: {location['latest']['deaths']}\n\nНаселение: {location['country_population']}\nПоследние обновление: {date[0]} {time[0]}''',
        color=0x0c0c0c
    )

    await ctx.send(embed = embed)


@bot.command()
async def gl( ctx, *, question ):
    url = 'https://google.gik-team.com/?q='
    emb = discord.Embed( title = question, description = 'Спасибо за использование!',
                         colour = discord.Color.green(), url = url + str(question).replace(' ', '+') )
    await ctx.send( embed = emb )

@bot.event
async def on_command_error(ctx, error):
    emb = discord.Embed(description = f'**:x: {ctx.author.name},Данной команды не существует.**', 
        color=0x0c0c0c)
    if isinstance(error, commands.CommandNotFound ):
        await ctx.send(embed = emb,delete_after= 5)         


@bot.command(aliases=['l'])
async def load(ctx, extension):
    extension = extension.lower()
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} загружен')


@bot.command(aliases=['unl'])
async def unload(ctx, extension):
    extension = extension.lower()
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} разгружен')

for filename in os.listdir("./cogs"):
    if filename.endswith(".py")and not filename.startswith("_"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.command(aliases=['sg'])
async def suggest_bot( ctx , * , agr ):
    suggest_chanell = bot.get_channel(951633154546999306) #Айди канала предложки
    embed = discord.Embed(title=f"{ctx.author.name} Предложил :", description= f" {agr} \n\n")

    embed.set_thumbnail(url=ctx.guild.icon_url)

    message = await suggest_chanell.send(embed=embed)
    await message.add_reaction('☑️')
    await message.add_reaction('❎')        

@bot.command(aliases=['rb'])
async def report_bug(ctx,*,arg = None):

    channel = bot.get_channel(952297146969911326) #Айди канала жалоб на баги

    if arg == None:
        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))
        return

    emb = discord.Embed(description =f'**:shield: {ctx.author.mention}, Вы отправили на рассмотрение жалобу о баге.', color=0x0c0c0c)
    await ctx.send(embed = emb)

    embed = discord.Embed(title =f"Жалоба на баг от {ctx.message.author.name}" ,description =f'{arg}', color=0x0c0c0c)
    await channel.send(embed = embed)    

@bot.command(aliases=['wall'])
async def wallpapers(ctx):
    img_url = nekos.img('wallpaper')
        
    emb = discord.Embed(description= f'Вот подобраные Вам обои.\n[Ссылка]({img_url})')
    emb.set_image(url= img_url)
    await ctx.send(embed=emb)

@bot.event
async def on_guild_join(guild): # событие подключения к серверу
    channel = guild.system_channel
    if channel == None:
        category = guild.categories[0]  
        chanel = category.channels[0] 
        await chanel.send("Хей это я Frebie Bot.")
    else:
        await channel.send("Хей это я Frebie Bot.")
    emb = discord.Embed(title = f"{guild.name}",description = "Новая гильдия", color=0x68fc97)
    emb.add_field(name= "Участники", value = f"{guild.member_count}")
    emb.add_field(name= "Создали", value = f"{guild.created_at.strftime('%#d, %b  %Y')}")
    emb.add_field(name = "Регион", value= f"{guild.region}")
    emb.add_field(name = "Верификация", value = f"{guild.verification_level}")
    emb.set_footer(text = f"ID:{guild.id}")
    logs = bot.get_channel(952311777251688568)
    await logs.send(embed = emb)

@bot.event
async def on_guild_remove(guild):
    emb = discord.Embed(title = f"Покинута гильдия\n{guild.name}", color = 0xeb512a)
    emb.description=(
        f"**Владелец**:{guild.owner}\n\n"
        f"**Участников**: {guild.member_count}\n\n"
        f"**Создана**:{guild.created_at.strftime('%#d, %b  %Y')}\n\n"
        f"**Регион**:{guild.region}\n\n"
        f"**Верефикация**:{guild.verification_level}\n\n")
    emb.set_footer(text = f"ID:{guild.id}")
    logs = bot.get_channel(952311777251688568)
    await logs.send(embed = emb)

@bot.command(name="бан", brief="Забанить пользователя на сервере", usage="ban <@user> <reason=None>", aliases=['b'])
@commands.has_permissions(ban_members=True)
async def бан(ctx, member: discord.Member, *, reason=None):
    await member.send(f"Ты был забанен на сервере") # Отправить личное сообщение пользователю
    await ctx.send(f"Member {member.mention} was banned on this server")
    await member.ban(reason=reason)


@bot.command(name="разбанить", brief="Разбанить пользователя на сервере", usage="unban <user_id>", aliases=['unb'])
@commands.has_permissions(ban_members=True)
async def разбан(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)

@bot.command(name="мут", brief="Запретить пользователю писать (настройте роль и канал)", usage="mute <member>", aliases=['m'])
async def mute_user(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.message.guild.roles, name="Muted")

    await member.add_roles(mute_role)
    await ctx.send(f"{ctx.author} выдал пользователю {member} мут")

@bot.command(description="Unmutes a specified user.", aliases=['unm'])
@commands.has_permissions(manage_roles=True)
async def размут(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"Пользователь {member.mention} успешно был снят мут!")
    await member.send(f"Вы были размьючены {ctx.guild.name}")

@bot.command(aliases=['st'])
@commands.has_permissions(manage_nicknames=True)
async def setnick(ctx, member:discord.Member,*,nick=None):
    old_nick = member.display_name

    await member.edit(nick=nick)

    new_nick = member.display_name

    await ctx.send(f'Changed nick from *{old_nick}* to *{new_nick}*')
    
@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx,*,reason='None'):
    channel =ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

    embed=discord.Embed(title=f'🔒 Locked',description=f'Reason: {reason}')

    await channel.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx,*,reason='None'):
    channel =ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    embed=discord.Embed(title=f'🔓 Unlocked',description=f'Reason: {reason}')
    await channel.send(embed=embed)

@bot.command(aliases=['sm'])
async def slowmode(ctx,sec:int=None,channel:discord.TextChannel=None):
    if not sec:
        sec=0
    if not channel:
        channel=ctx.channel

    await channel.edit(slowmode_delay=sec)

    await channel.send(f'This channel is now on **{sec}s** slowmode')
    
    
bot.run("Your Token")
