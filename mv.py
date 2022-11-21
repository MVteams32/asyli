import discord
import asyncio
import random
import datetime
import time
from discord.ext import commands, tasks
from discord.ext.commands import check
from discord.ui import InputText, Modal, Button, Select, View
from quickdb import SQLITE

db = SQLITE()

client = commands.Bot(command_prefix="*", intents = discord.Intents.all())

answer_words = [ '<@1014449986156638338>' ]

@client.event
async def on_member_join(member):
    logchannel = db.get(f"logchannel_{member.guild.id}") 
    channel = await client.fetch_channel(logchannel)
    asyli = discord.Embed(title="Вход на сервер", description=f"{member.name} вошёл на сервер", color=0x0050ff)
    await channel.send(embed=asyli)
    await member.add_roles(role)

@client.event
async def on_guild_join(guild: discord.Guild):
    channel = await client.fetch_channel(1037036226219364364)
    asyli = discord.Embed(title="Добавили",description=f"Меня добавили на сервер!\nСервер айди: **{guild.id}**", color=0x0050ff)
    await channel.send(embed=asyli)

@client.event
async def on_guild_remove(guild: discord.Guild):
    channel = await client.fetch_channel(1037036226219364364)
    asyli = discord.Embed(title="Выгнали",description=f"Меня кикнули из сервера\nСервер айди: **{guild.id}**", color=0x0050ff)
    await channel.send(embed=asyli)

@client.event
async def on_member_join(member):
    current = db.get(f'antibot_{member.guild.id}')
    logchannel = db.get(f"logchannel_{member.guild.id}") 
    if current == 'on' and member.bot and not member.public_flags.verified_bot:
        await member.kick(reason = 'Сработала защита от неверифицированных ботов')   
        channel = await client.fetch_channel(logchannel)
        asyli = discord.Embed(title="Сработала система", description=f"Кикнули бота на сервере\nСервер айди: **{member.guild.id}**", color=0x0050ff)
        await channel.send(embed=asyli)

@client.event
async def on_message_delete(message):
  logchannel = db.get(f"logchannel_{message.guild.id}")
  channel = await client.fetch_channel(logchannel)
  asyli = discord.Embed(title = f"Сообщение удалено!", description = f"Удаленно сообщение в <#{message.channel.id}>\nУдалил: {message.member.name}\nСодержание сообщения:\n```{message.content}```", color=0x0050ff)
  await channel.send(embed=asyli)

@client.event
async def on_message_edit(before: discord.Message, after: discord.Message):
  logchannel = db.get(f"logchannel_{before.guild.id}")
  channel = await client.fetch_channel(logchannel)
  asyli = discord.Embed(title = f"Изменение!", description = f"{before.author.name} изменил сообщение, в канале <#{before.channel.id}>", color=0x0050ff)
  asyli.add_field(name="Было:", value=f"```{before.content}```")
  asyli.add_field(name="Стало:", value=f"```{after.content}```")
  await channel.send(embed=asyli)

@client.event
async def on_message(msg):
    current = db.get(f'antilinks_{msg.guild.id}')
    guild = msg.guild
    mutedRole = discord.utils.get(guild.roles, name="As-muted")
    if current == 'on':
        if msg in asyli_discord:
            await member.add_roles(mutedRole, reason = 'Сработала защита от ссылк')
            logchannel = db.set(f"logchannel_{msg.guild.id}")
            channel = await client.fetch_channel(logchannel)
            asyli = discord.Embed(title="Сработала система", description=f"Замьютили учасиника на сервере\nСервер айди: **{member.guild.id}**", color=0x0050ff)
            await channel.send(embed=asyli)

@client.event
async def on_message(msg):
    xkey = f'xp_{msg.guild.id}_{msg.author.id}'
    lkey = f'lvl_{msg.guild.id}_{msg.author.id}'
    xp = int(db.get(xkey) or 0)
    lvl = int(db.get(lkey) or 1)
    
    if xp >= lvl * 10:
        db.set(xkey, 0)
        db.add(lkey, 1)
        return await msg.send(f'{msg.author.mention}, вы повысили уровень!')
    db.add(xkey, 1) 

@client.event
async def on_message( message ):
    msg = message.content.lower()

    if msg in answer_words:
        asyli = discord.Embed(title="Слэш-команды: /", color=0x0050ff)
        await message.channel.send(embed=asyli)

@client.event
async def on_ready():
    print('AsyliBot Успешно запущен!')
    await client.change_presence(status=discord.Status.dnd,
                                    activity=discord.Streaming(name=f"{len(set(client.get_all_members()))} участников",
                                        url='https://twitch.tv/404'))

class MyModalo(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Ваш ник с тегом.", placeholder="Например MVXXL#9919."))

        self.add_item(InputText(label="Ваша оценка", placeholder="От 0/10"))

        self.add_item(
            InputText(
                label="Оставьте отзыв.",
                placeholder="Тут напишите свой отзыв.",
                style=discord.InputTextStyle.long,
            )
        )


    async def callback(self, interaction: discord.Interaction):
        accountset = db.get(f"accountset_{interaction.guild.id}")
        if accountset == None:
            asyli = discord.Embed(title="вы не установили канал с отправкой сообщения от команды", color=0x0050ff)
            await interaction.response.send_message(embeds=[asyli])
        else:
            channel = await client.fetch_channel(accountset)
            asyli = discord.Embed(title="Заявка на оценку сотрудника", color=0x0050ff)
            asyli.add_field(name="Ник пользователя", value=self.children[0].value, inline=False)
            asyli.add_field(name="Оценка роботы", value=self.children[1].value, inline=False)
            asyli.add_field(name="Отзыв", value=self.children[2].value, inline=False)
            await channel.send(embeds=[asyli])
            asyli = discord.Embed(title="Успешно!", description="Вы успешно отправили свой отзыв", color=0x0050ff)
            await interaction.response.send_message(embeds=[asyli])

@client.slash_command(name = "account", description = "Остаить отзыв")
async def account(ctx):
    modal = MyModalo(title="Отзыв")
    await ctx.send_modal(modal)

@client.slash_command(name = "set_account", description = "Установить канал для отзывов")
@commands.has_permissions(administrator = True)
async def set_account(ctx, channel: discord.TextChannel):
    db.set(f"accountset_{ctx.guild.id}", int(channel.id))
    asyli = discord.Embed(title = "Установка канала", description = f"Вы успешно установили канал <#{channel.id}> в качестве канала для отправки отзывов!", color=0x0050ff)
    await ctx.send(embed=asyli)

@set_account.error
async def set_account_error(interaction, error):
        if isinstance(error, commands.BotMissingPermissions):
                await interaction.response.send_message(embed=discord.Embed(
                    f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

        elif isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message(
                embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                        f"команды, требуемые права: "
                                        f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

class MyModalorep(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Ваш ник с тегом.", placeholder="Например MVXXL#9919."))

        self.add_item(InputText(label="Тема", placeholder="Например тема бага команда report"))

        self.add_item(
            InputText(
                label="Оставьте баг или ошибку.",
                placeholder="Баг/ошибка/граматика/другое.",
                style=discord.InputTextStyle.long,
            )
        )


    async def callback(self, interaction: discord.Interaction):
        channel = await client.fetch_channel(1040679807165403236)
        asyli = discord.Embed(title="Report!", description=f"Ник пользователя: {interaction.user.name} | {interaction.user.id}", color=0x0050ff)
        asyli.add_field(name="Тема бага:", value=self.children[1].value, inline=False)
        asyli.add_field(name="Баг:", value=self.children[2].value, inline=False)
        asyli.set_thumbnail(url=interaction.user.avatar.url)
        asyli.set_footer(icon_url="https://media.discordapp.net/attachments/1033387036209598554/1041765467834032228/image-removebg-preview.png", text=f'Asyli bot | Support')
        await channel.send(embed=asyli)
        asyli = discord.Embed(title="Успешно!", description="Вы успешно отправили свой баг", color=0x0050ff)
        await interaction.response.send_message(embeds=[asyli], ephemeral=True)

@client.slash_command(name = "report", description = "Отаправить баг в боте.")
@commands.cooldown(1, 43200, commands.BucketType.user)
async def report(ctx):
    modal = MyModalorep(title="Доклад на баги")
    await ctx.send_modal(modal)

@report.error
async def report_error(ctx, error):
     if isinstance(error, commands.CommandOnCooldown):
        asyli = discord.Embed(title="Ошибка!", description=f"Вы сможете использовать команду через `{error.retry_after:.2f}`", color=0x0050ff)
        await ctx.response.send_message(embed=asyli, ephemeral=True)

class MyModalu(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Ваш ник с тегом.", placeholder="Например MVXXL#9919."))

        self.add_item(InputText(label="На какую должность?", placeholder="Например helper."))

        self.add_item(InputText(label="Готовы пройди дополнительный опрос?", placeholder="Да/Нет.", min_length=2, max_length=100))

        self.add_item(InputText(label="Почему мы должны взять именно вас?", placeholder="Например Я такой вот и такой вот."))

        self.add_item(InputText(label="Сколько готовы работать на сервере?", placeholder="Например 3часа."))

    async def callback(self, interaction: discord.Interaction):
        jobset = db.get(f"jobset_{interaction.guild.id}")
        if jobset == None:
            asyli = discord.Embed(title="вы не установили канал с отправкой сообщения от команды", color=0x0050ff)
            await interaction.response.send_message(embeds=[asyli])
            asyli = discord.Embed(title="Заявка на должность", color=0x0050ff)
            asyli.add_field(name="Ник пользователя", value=self.children[0].value, inline=False)
            asyli.add_field(name="Должность", value=self.children[1].value, inline=False)
            asyli.add_field(name="Имя пользователя", value=self.children[2].value, inline=False)
            asyli.add_field(name="Почемы вы должни взять меня", value=self.children[3].value, inline=False)
            asyli.add_field(name="Возможность работать на сервере", value=self.children[4].value, inline=False)
            await channel.send(embed=asyli)
        else:
            channel = await client.fetch_channel(jobset)
            asyli = discord.Embed(title="вы не установили канал с отправкой сообщения от команды", color=0x0050ff)
            await interaction.response.send_message(embeds=[asyli])
            asyli = discord.Embed(title="Успешно!", description="Вы успешно отправили свою заявку на работу", color=0x0050ff)
            await interaction.response.send_message(embeds=[asyli])

@client.slash_command(name = "job", description = "Отаправить заявку")
async def job(ctx):
    modal = MyModalu(title="Заявка на роботу")
    await ctx.send_modal(modal)

@client.slash_command(name = "set_job", description = "Установить канал для работ")
@commands.has_permissions(administrator = True)
async def set_job(ctx, channel: discord.TextChannel):
    db.set(f"jobset_{ctx.guild.id}", int(channel.id))
    asyli = discord.Embed(title = "Установка канала", description = f"Вы успешно установили канал <#{channel.id}> в качестве канала для отправки заявкок на работу!", color=0x0050ff)
    await ctx.send(embed=asyli)

@set_job.error
async def set_job_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

class MyModale(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Ваш ник", placeholder="Например: MVXXL#9919."))

        self.add_item(InputText(label="Идея", placeholder="Например: добавить меня"))

    async def callback(self, interaction: discord.Interaction):
        ideas = db.get(f"ideaset_{interaction.guild.id}")
        if ideas == None:
            asyli = discord.Embed(title="вы не установили канал с отправкой сообщения от команды", color=0x0050ff)
            await interaction.response.send_message(embeds=[asyli])
        else:
            channel = await client.fetch_channel(ideas)
            asyli = discord.Embed(title="Идеи", color=0x0050ff)
            asyli.add_field(name="Ник автора", value=self.children[0].value, inline=False)
            asyli.add_field(name="Идея", value=self.children[1].value, inline=False)
            await channel.send(embed=asyli)
            asyli = discord.Embed(title="Успешно!", description="Вы успешно отправили свою идею", color=0x0050ff)
            await interaction.response.send_message(embeds=[asyli])

@client.slash_command(name = "ideas", description = "Ввести Идею")
async def ideas(ctx):
    modal = MyModale(title="ideas")
    await ctx.send_modal(modal)

@client.slash_command(name = "set_ideas", description = "Установить канал для идей")
@commands.has_permissions(administrator = True)
async def set_ideas(ctx, channel: discord.TextChannel):
    db.set(f"ideaset_{ctx.guild.id}", int(channel.id))
    asyli = discord.Embed(title = "Установка канала", description = f"Вы успешно установили канал <#{channel.id}> в качестве канала для отправки идей!", color=0x0050ff)
    await ctx.send(embed=asyli)

@set_ideas.error
async def set_ideas_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

class MyModalr(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Ваш ник", placeholder="Например: MVXXL#9919."))

        self.add_item(InputText(label="Ник нарушителя", placeholder="Например: MVXXL#9919."))

        self.add_item(InputText(label="Жалоба на нарушителя", placeholder="Например: он нарушил правило 1.6", style=discord.InputTextStyle.long,))


    async def callback(self, interaction: discord.Interaction):
        appeal = db.get(f"appealset_{interaction.guild.id}")
        if appeal == None:
            asyli = discord.Embed(title="вы не установили канал с отправкой сообщения от команды", color=0x0050ff)
            await interaction.response.send_message(embeds=[asyli])
        else:
            channel = await client.fetch_channel(appeal)
            asyli = discord.Embed(title="Идеи", color=0x0050ff)
            asyli.add_field(name="Ник пользователя", value=self.children[0].value, inline=False)
            asyli.add_field(name="Ник нарушителя", value=self.children[1].value, inline=False)
            asyli.add_field(name="Жалоба", value=self.children[2].value, inline=False)
            await channel.send(embed=asyli)
            asyli = discord.Embed(title="Успешно!", description="Вы успешно отправили свою жалобу", color=0x0050ff)
            await interaction.response.send_message(embeds=[asyli])

@client.slash_command(name = "appeal", description = "Кинуть жалобу")
async def appeal(ctx):
    modal = MyModalr(title="Жалоба")
    await ctx.send_modal(modal)

@client.slash_command(name = "set_appeal", description = "Установить канал для жалоб")
@commands.has_permissions(administrator = True)
async def set_appeal(ctx, channel: discord.TextChannel):
    db.set(f"appealset_{ctx.guild.id}", int(channel.id))
    asyli = discord.Embed(title = "Установка канала", description = f"Вы успешно установили канал <#{channel.id}> в качестве канала для отправки жалоб!", color=0x0050ff)
    await ctx.send(embed=asyli)

@set_appeal.error
async def set_appeal_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

@client.slash_command(name = "ban", description = "Забанить участника")
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: Option(discord.Member), reason="Не указано"):
    logchannel = db.get(f"logchannel_{ctx.guild.id}") 
    await member.ban(reason = reason)
    asyli = discord.Embed(title="Участник был забанен!", color = 0x0050ff)
    asyli.add_field(name = "Админ", value=f" <@{ctx.author.id}>")
    asyli.add_field(name = "Забаненный", value=f" <@{member.id}>")
    asyli.add_field(name=f"Причина: ", value=f"{reason}")
    await ctx.send(embed=asyli)
    asyli = discord.Embed(title="Вы забанены!", description=f"**Модератор:** <@{interaction.author.id}>\n\n**Причина:**\n{reason}", color=0x0000)
    button = Button(label=f"Отправленно с {interaction.guild}", style=discord.ButtonStyle.blurple, emoji="📨", disabled=True)
    view = View()
    view.add_item(button)
    await member.send(embed=asyli, view=view)
    await member.send(embed=asyli)
    if logchannel == None:
        channel = await client.fetch_channel(1033387036209598554)
        asyli = discord.Embed(title = f"Канала нету", description = f"У вас нету канала для логов", color=0x0050ff)
        await channel.send(embed=asyli)
    else:
        channel = await client.fetch_channel(logchannel)
        asyli = discord.Embed(title = f"{member} был забанен", description = f"Модератор: {ctx.author.name}\n В {datetime.datetime.now}", color=0x0050ff)
        await channel.send(embed=asyli)

@client.slash_command(name = "editname", description = "зменить имя сервера")
@commands.has_permissions(kick_members = True)
async def editname(ctx: commands.Context, name: str):
    logchannel = db.get(f"logchannel_{ctx.guild.id}") 
    await ctx.guild.edit(name=name, reason=str(ctx.author))
    asyli = discord.Embed(title="Переименование сервера", color = 0x0050ff, description=f"Название сервера изменено на {name}!")
    await ctx.send(embed=asyli)
    if logchannel == None:
        channel = await client.fetch_channel(1033387036209598554)
        asyli = discord.Embed(title = f"Канала нету", description = f"У вас нету канала для логов", color=0x0050ff)
        await channel.send(embed=asyli)
    else:
        channel = await client.fetch_channel(logchannel)
        asyli = discord.Embed(title = f"Извенено название сервера", description = f"Редактор: {ctx.author.name}\nНазвание: {name}\n В {datetime.datetime.now}", color=0x0050ff)
        await channel.send(embed=asyli)

@editname.error
async def editname_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

@client.slash_command(name = "botinfo", description = "Информация о боте")
async def botinfo(ctx):
    asyli = discord.Embed(title = "Инфо о боте!", description = f"", color = 0x0050ff)
    asyli.add_field(name="Серверов: ", value=f"```{len(client.guilds)}```")
    asyli.add_field(name="Имя бота: ", value=f"```{client.user.name}```")
    asyli.add_field(name="Владелец бота: ", value=f"```MVXXL#9919```")
    asyli.add_field(name="Пинг бота: ", value=f"```{round(client.latency * 1000)}ms```")
    asyli.add_field(name="Язык бота: ", value=f"```Python 3.10.7```")
    asyli.add_field(name="Библиотека бота: ", value=f"```Pycord 2.2.2```")
    asyli.add_field(name="Префикс: ", value=f"```'/' слэш-команды```")
    asyli.add_field(name="Версия бота: ", value=f"```0.19.0```")
    asyli.add_field(name="Участников: ", value=f"```{len(set(client.get_all_members()))}```")
    button = Button(label="Пригласить бота", url="https://discord.com/api/oauth2/authorize?client_id=1014449986156638338&permissions=8&scope=bot"+"%"+"20applications.commands")
    button1 = Button(label="Cервер поддержки", url="https://discord.gg/yKv6PBUmcu")
    
    view = View()
    view.add_item(button)
    view.add_item(button1)
    await ctx.send(embed=asyli, view=view)

@client.slash_command(name = "numbergama", description = "Игра с числом")
async def numbergama(ctx, number):
    numb = random.randint(1, 10)
    if int(number) == numb:
        asyli = discord.Embed(title="Ты угадал число!", description=f"Моё число: {numb}", color = 0x52ff00)
        await ctx.send(embed=asyli)
    else:
        asyli = discord.Embed(title=f"Не совпадает!", description=f"Твоё число: {number}\nМоё число: {numb}", color = 0xff0000)
        await ctx.send(embed=asyli)

@client.slash_command(name = "say", description = "Сказать от бота")
async def say(ctx, title, description = None):
    vip = db.get(f'vip_{ctx.guild.id}')
    if vip == None:
        asyli = discord.Embed(title="Как так?", description = f"Это вип команда.\nЕсли вы хотите вип на вашем серевере свяжитесь с `MVXXL#9919`", color = 0x0050ff)
        asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299204393836625/free-icon-danger-5885380-removebg-preview.png")
        await ctx.send(embed=asyli)
    else:
        if description == None:
            asyli = discord.Embed(title=f"{title}", color = 0x0050ff)
            await ctx.send(embed=asyli) 
        else:
            asyli = discord.Embed(title=f"{title}", description=f"{description}", color = 0x0050ff)
            await ctx.send(embed=asyli)

@client.slash_command(name = "slowmode", description = "Поставить задержку в канале")
@commands.has_permissions(administrator = True)
async def slowmode(ctx, seconds: int):
    logchannel = db.get(f"logchannel_{ctx.guild.id}") 
    await ctx.channel.edit(slowmode_delay=seconds)
    asyli = discord.Embed(title = "Изменение канала", description = f"Установленна задержка на {seconds} seconds!", color = 0x0050ff)
    await ctx.send(embed=asyli)
    if logchannel == None:
        channel = await client.fetch_channel(1033387036209598554)
        asyli = discord.Embed(title = f"Канала нету", description = f"У вас нету канала для логов", color=0x0050ff)
        await channel.send(embed=asyli)
    else:
        channel = await client.fetch_channel(logchannel)
        asyli = discord.Embed(title = f"Изменена задержка канала", description = f"Редактор: {ctx.author.name}\nЗадержка на {seconds}\n В {datetime.datetime.now}", color=0x0050ff)
        await channel.send(embed=asyli)

@slowmode.error
async def slowmode_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

@client.slash_command(name = "vote", description = "Голосование по реакциям")
@commands.has_permissions(administrator = True)
async def vote(ctx, reason):
    if reason == None:
        reason = f"Нет причины для голосования {ctx.author}"
    uu = await ctx.send(discord.Embed(title="Голосование", description=f"**Проголосуйте ниже!**\n {reason}", color = 0x0050ff))
    await uu.add_reaction("<a:emoji_49:949717185075486781>")
    await uu.add_reaction("<a:emoji_49:949717214301401090>")

@vote.error
async def vote_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

@client.slash_command(name = "kick", description = "Кикнуть участника")
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: Option(discord.Member), reason):
    logchannel = db.get(f"logchannel_{ctx.guild.id}") 
    if reason == None:
        reason = f"Нет причины кика {ctx.author}"
    await member.kick(reason = reason)
    asyli = discord.Embed(title="Участник кикнут с сервера", description=f"Админ: <@{ctx.author.id}>\n Кикнутый: <@{member.id}>\n Причина: {reason}", color = 0x0050ff)
    await ctx.send(embed=asyli)
    if logchannel == None:
        channel = await client.fetch_channel(1033387036209598554)
        asyli = discord.Embed(title = f"Канала нету", description = f"У вас нету канала для логов", color=0x0050ff)
        await channel.send(embed=asyli)
    else:
        channel = await client.fetch_channel(logchannel)
        asyli = discord.Embed(title = f"{member} был кикнут", description = f"Модератор: {ctx.author.name}\n В {datetime.datetime.now}", color=0x0050ff)
        await channel.send(embed=asyli)

@kick.error
async def error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

@client.slash_command(name = "wink", description = "Подмигивать")
async def wink(ctx, member: Option(discord.Member)):
    vip = db.get(f'vip_{ctx.guild.id}')
    if vip == None:
        asyli = discord.Embed(title="Как так?", description = f"Это вип команда.\nЕсли вы хотите вип на вашем серевере свяжитесь с `MVXXL#9919`", color = 0x0050ff)
        asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299204393836625/free-icon-danger-5885380-removebg-preview.png")
        await ctx.send(embed=asyli)
    else:    
        asyli = discord.Embed(description=f"<@{ctx.author.id}> **подмигивает** <@{member.id}>", color = 0x0050ff)
        asyli.set_image(url=random.choice(['https://i.some-random-api.ml/pQgRTo2ftP.gif', 'https://i.some-random-api.ml/7Rr2P6EZaw.gif', 'https://i.some-random-api.ml/JrJkutMyGT.gif', 'https://i.some-random-api.ml/8IpOOISRNf.gif', 'https://i.some-random-api.ml/EwpNmiJLW4.gif', 'https://i.some-random-api.ml/pHJ6jx0kLl.gif', 'https://i.some-random-api.ml/Sp31pB0jEJ.gif', 'https://i.some-random-api.ml/Ed6eHodbYh.gif', 'https://i.some-random-api.ml/0b1UVUE7tJ.gif', 'https://i.some-random-api.ml/74EJtSs048.gif']))
        await ctx.send(embed=asyli)

@client.slash_command(name = "pat", description = "Погладить кого-то")
async def pat(ctx, member: Option(discord.Member)):
    vip = db.get(f'vip_{ctx.guild.id}')
    if vip == None:
        asyli = discord.Embed(title="Как так?", description = f"Это вип команда.\nЕсли вы хотите вип на вашем серевере свяжитесь с `MVXXL#9919`", color = 0x0050ff)
        asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299204393836625/free-icon-danger-5885380-removebg-preview.png")
        await ctx.send(embed=asyli)
    else:
        asyli = discord.Embed(description=f"<@{ctx.author.id}> **погладил(а)** <@{member.id}> ", color = 0x0050ff)
        asyli.set_image(url=random.choice(['https://i.some-random-api.ml/TqydRNWuJE.gif', 'https://i.some-random-api.ml/LUzNCa6O67.gif', 'https://i.some-random-api.ml/UH3WgKYYje.gif', 'https://i.some-random-api.ml/eT58KYZl8I.gif', 'https://i.some-random-api.ml/mPOieKyr54.gif', 'https://i.some-random-api.ml/FWGXnZJPzT.gif', 'https://i.some-random-api.ml/8ZURLZ5h6i.gif', 'https://i.some-random-api.ml/lNOdTaOntw.gif', 'https://i.some-random-api.ml/Fn25NreFSH.gif', 'https://i.some-random-api.ml/Bleo3pQIp8.gif', 'https://i.some-random-api.ml/OIFIogbfPO.gif']))
        await ctx.send(embed=asyli)

@client.slash_command(name = "punch", description = "Ударить кого-тo")
async def punch(ctx, member: Option(discord.Member)):
    vip = db.get(f'vip_{ctx.guild.id}')
    if vip == None:
        asyli = discord.Embed(title="Как так?", description = f"Это вип команда.\nЕсли вы хотите вип на вашем серевере свяжитесь с `MVXXL#9919`", color = 0x0050ff)
        asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299204393836625/free-icon-danger-5885380-removebg-preview.png")
        await ctx.send(embed=asyli)
    else:
        asyli = discord.Embed(description=f"<@{ctx.author.id}> **ударил(а)** <@{member.id}> ", color = 0x0050ff)
        asyli.set_image(url=random.choice(['https://c.tenor.com/6a42QlkVsCEAAAAM/anime-punch.gif', 'https://c.tenor.com/BoYBoopIkBcAAAAM/anime-smash.gif', 'https://c.tenor.com/pHCT4ynbGIUAAAAM/anime-girl.gif', 'https://c.tenor.com/p_mMicg1pgUAAAAM/anya-forger-damian-spy-x-family.gif', 'https://c.tenor.com/p3Hgg8D0mFMAAAAM/anime-punch.gif', 'https://c.tenor.com/D4D8Xj2rqzoAAAAM/anime-punch.gif', 'https://c.tenor.com/hirgW74gX1AAAAAM/punch-kick.gif', 'https://c.tenor.com/dLaisLGeL1cAAAAM/shy-punch.gif', 'https://c.tenor.com/6pY8YkmSCpcAAAAM/shiki-granbell-shiki-punching.gif', 'https://c.tenor.com/s0bU-NO1QIQAAAAM/anime-punch.gif', 'https://c.tenor.com/jMVkUG5ouL8AAAAM/punch-anime.gif', 'https://c.tenor.com/LR7jMiTMwmAAAAAM/jealous-punching.gif', 'https://c.tenor.com/wYyB8BBA8fIAAAAM/some-guy-getting-punch-anime-punching-some-guy-anime.gif', 'https://c.tenor.com/EvBn8m3xR1cAAAAM/toradora-punch.gif', 'https://c.tenor.com/SwMgGqBirvcAAAAM/saki-saki-kanojo-mo-kanojo.gif']))
        await ctx.send(embed=asyli)

@client.slash_command(name = "hug", description = "Обнять кого-тo")
async def hug(ctx, member: Option(discord.Member)):
    vip = db.get(f'vip_{ctx.guild.id}')
    if vip == None:
        asyli = discord.Embed(title="Как так?", description = f"Это вип команда.\nЕсли вы хотите вип на вашем серевере свяжитесь с `MVXXL#9919`", color = 0x0050ff)
        asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299204393836625/free-icon-danger-5885380-removebg-preview.png")
        await ctx.send(embed=asyli)
    else:
        asyli = discord.Embed(description=f"<@{ctx.author.id}> **обнял(а)** <@{member.id}>", color = 0x0050ff)
        asyli.set_image(url=random.choice(['https://c.tenor.com/0vl21YIsGvgAAAAM/hug-anime.gif', 'https://c.tenor.com/1T1B8HcWalQAAAAM/anime-hug.gif', 'https://c.tenor.com/AvXyGGhalDsAAAAM/anime-hug.gif', 'https://c.tenor.com/DVOTqLcB2jUAAAAM/anime-hug-love.gif', 'https://c.tenor.com/-3I0yCd6L6AAAAAM/anime-hug-anime.gif', 'https://i.some-random-api.ml/EkRec1cnA8.gif', 'https://i.some-random-api.ml/eM56DKbh89.gif', 'https://i.some-random-api.ml/ozeHK135ai.gif', 'https://i.some-random-api.ml/zSKMG85bIg.gif', 'https://i.some-random-api.ml/4lsHtTeodH.gif"', 'https://i.some-random-api.ml/52EStsWOxD.gif', 'https://i.some-random-api.ml/IId0dr4Gdd.gif', 'https://i.some-random-api.ml/KFLpKFvCS1.gif', 'https://i.some-random-api.ml/xuDnvZuy9q.gif', 'https://i.some-random-api.ml/dPLEGVVbIS.gif']))
        await ctx.send(embed=asyli)

@client.slash_command(name = "msg", description = "Отправить сообщение участнику.")
async def msg(ctx, member: discord.Member, message):
    if message == None:
        asyli = discord.Embed(title = "ошибка!", description='Вы забыли ввести сообщение!', color = 0xf30808)
        asyli.set_footer(text=f"Почта Asyli быстро и надёжно!")
        await ctx.send(embed = asyli)
    elif member == None:
        asyli = discord.Embed(title = "ошибка!", description='Вы забыли ввести ник пользователя!', color = 0xf30808)
        asyli.set_footer(text=f"Почта Asyli быстро и надёжно!")
        await ctx.send(embed = asyli)
    else:
        asyli = discord.Embed(title = 'Вам письмо!', description=f"{message}", color=0x0050ff)
        asyli.set_footer(text=f"Почта Asyli быстро и надёжно!")
        await member.send(embed=asyli)     
    asyli = discord.Embed(title = 'Сообщение было доставлено!')
    asyli.set_footer(text=f"Почта Asyli быстро и надёжно!")
    await ctx.response.send_message(embed=asyli,ephemeral=True)

class MenuOnHelp(Select):
    def __init__(self) -> None:
        super().__init__(
            options=[
            discord.SelectOption(label="Заявочные", description="Заявочные команды"),
            discord.SelectOption(label="Модерация", description="Бан, кик, и другие настройки"),
            discord.SelectOption(label="Фан", description="Фан команды обнять и другое"),
            discord.SelectOption(label="Установки", description="Что устанавливаит команды?!"),
            discord.SelectOption(label="Экономика", description="Что устанавливаит команды?!"),
            discord.SelectOption(label="Вип", description="Оу дорого багато)"),
            discord.SelectOption(label="Другие", description="Ещё больше команд!") 
            ]
        )
    async def callback(self, interaction):
        if self.values[0] == "Заявочные":
            asyli = discord.Embed(title="Категория Заявочные", color=0x0050ff)
            asyli.add_field(name="/account", value="```Оставить заявку отзыв.```")
            asyli.add_field(name="/appeal", value="```Отправить заявку жалобу.```")
            asyli.add_field(name="/ideas", value="```Отправить заявку идею.```")
            asyli.add_field(name="/job", value="```Отправить заявку на работу.```")
            asyli.add_field(name="Все команды категории", value="```/account, /appeal, /ideas, /job.```")
            asyli.set_footer(text=f"Если каких то команды нету в хелпе пишите /report")
            await interaction.response.send_message(embed=asyli,ephemeral=True)
        elif self.values[0] == "Модерация":
            asyli = discord.Embed(title="Категория Модерация", color=0x0050ff)
            asyli.add_field(name="/ban", value="```Забанить участника.```")
            asyli.add_field(name="/editname", value="```Изменить название сервера.```")
            asyli.add_field(name="/slowmode", value="```Установить задержку сообщений в канале.```")
            asyli.add_field(name="/kick", value="```Кикнуть участника.```")
            asyli.add_field(name="/warn", value="```Выдать предупреждение.```")
            asyli.add_field(name="/warns", value="```Помотреть предупреждения.```")
            asyli.add_field(name="/unwarn", value="```Снять предупреждение.```")
            asyli.add_field(name="/antibot", value="```Кикать неверифицированных ботов```")
            asyli.add_field(name="/antibot", value="```Мутить за приглшения серверов дискорд.```")
            asyli.add_field(name="/clear", value="```Очистить чат.```")
            asyli.add_field(name="/vote", value="```Устроить голосование.```")
            asyli.add_field(name="/mute", value="```Выдать time-out.```")
            asyli.add_field(name="/unmute", value="```Снять time-out.```")
            asyli.add_field(name="/rolemute", value="```Выдать мтют ролью.```")
            asyli.add_field(name="/unrolemute", value="```Снять мьют ролевой.```")
            asyli.add_field(name="Все команды категории", value="```/ban, /editname, /slowmode, /kick, /warn, /unwarn, /antibot, /clear, /vote, /mute, /unmute, /rolemute, /unrolemute.```")
            asyli.set_footer(text=f"Если каких то команды нету в хелпе пишите /report")
            await interaction.response.send_message(embed=asyli,ephemeral=True)
        elif self.values[0] == "Фан":
            asyli = discord.Embed(title="Категория фан", color=0x0050ff)
            asyli.add_field(name="/pat", value="```Погладить участника.```")
            asyli.add_field(name="/hug", value="```Обнять участника.```")
            asyli.add_field(name="/panch", value="```Ударить участника.```")
            asyli.add_field(name="/wink", value="```Подмигивать участнику.```")
            asyli.add_field(name="Все команды категории", value="```/pat, /hug, /panch, /wink.```")
            asyli.set_footer(text=f"Если каких то команды нету в хелпе пишите /report")
            await interaction.response.send_message(embed=asyli,ephemeral=True)
        elif self.values[0] == "Установки":
            asyli = discord.Embed(title="Категория Установки", color=0x0050ff)
            asyli.add_field(name="/set_emoji_economy", value="```Установить емоджи экономики.```")
            asyli.add_field(name="/set_log_channel", value="```Установить канал с логами.```")
            asyli.add_field(name="/set_appeal", value="```Установить канал для жалоб.```")
            asyli.add_field(name="/set_account", value="```Установть канал для отзывов.```")
            asyli.add_field(name="/set_ideas", value="```Установить канал для идей.```")
            asyli.add_field(name="/set_job", value="```Установить канал для заявок робот```")
            asyli.add_field(name="Все команды категории", value="```/set_emoji_economy, /set_log_channel, /set_appeal, /set_account, /set_ideas, /set_job.```")
            asyli.set_footer(text=f"Если каких то команды нету в хелпе пишите /report")
            await interaction.response.send_message(embed=asyli,ephemeral=True)
        elif self.values[0] == "Вип":
            asyli = discord.Embed(title="Категория Вип", color=0x0050ff)
            asyli.add_field(name="/say", value="Отправить новости.")
            asyli.add_field(name="Все команды категории", value="```/say.```")
            asyli.set_footer(text=f"Если каких то команды нету в хелпе пишите /report")
            await interaction.response.send_message(embed=asyli,ephemeral=True)
        elif self.values[0] == "Экономика":
            asyli = discord.Embed(title="Категория Экономика", color=0x0050ff)
            asyli.add_field(name="/work", value="```Команда работать что бы полуть зарплату.```")
            asyli.add_field(name="/timely", value="```Команда которую можно использовать 1 раз в 12ч.```")
            asyli.add_field(name="/casino", value="```Команда что бы поиграть в казино.```")
            asyli.add_field(name="/add_money", value="```Команда что бы начислить деньги.```")
            asyli.add_field(name="/remove_money", value="```Команда что бы снять деньги.```")
            asyli.add_field(name="/balance", value="```Команда что бы проверить баланс.```")
            asyli.add_field(name="/shop", value="```Команда что бы посмотреть предметы в магазине.```")
            asyli.add_field(name="/buy", value="```Команда что бы купить что-то в магазине.```")
            asyli.add_field(name="/create_item", value="```Команда что бы создать предмет в магазине.```")
            asyli.add_field(name="/remove_item", value="```Команда что бы убрать предмет в магазине.```")
            asyli.add_field(name="Все команды категории", value="```/work, /timely, /casino, /add_money, /remove_money, /balance, /shop, /buy, /create_item, /remove_item.```")
            asyli.set_footer(text=f"Если каких то команды нету в хелпе пишите /report")
            await interaction.response.send_message(embed=asyli,ephemeral=True)
        elif self.values[0] == "Другие":
            asyli = discord.Embed(title="Категория Другие", color=0x0050ff)
            asyli.add_field(name="/help", value="```Команда помощи.```")
            asyli.add_field(name="/avatar", value="```Команда просмотр аватара.```")
            asyli.add_field(name="/click", value="```Кликать.```")
            asyli.add_field(name="/clicks", value="```Профиль кликов.```")
            asyli.add_field(name="/add_click", value="```Добавить кликов.```")
            asyli.add_field(name="/remove_click", value="```Снять клики.```")
            asyli.add_field(name="/addrole", value="```Добавить роль.```")
            asyli.add_field(name="/afk", value="```Поставить афк.```")
            asyli.add_field(name="/botinfo", value="```Просмотреть информацию о боте.```")
            asyli.add_field(name="/create_notes", value="```Создать заметку.```")
            asyli.add_field(name="/me_notes", value="```Посмтореть **свои** заметки.```")
            asyli.add_field(name="/remove_notes", value="```Убрать свою заметку.```")
            asyli.add_field(name="/msg", value="```Отправть сообщение участнику в лс.```")
            asyli.add_field(name="/new_nick", value="```Поставить новый ник.```")
            asyli.add_field(name="/numbergame", value="```Сиграть в угдай число.```")
            asyli.add_field(name="/partnerbot", value="```Подать партнёрство и согласиться на условия.```")
            asyli.add_field(name="/user", value="```Просмотреть инфу о человеке.```")
            asyli.add_field(name="/report", value="```Отправить доклад то что не корректно работает.```")
            asyli.add_field(name="Все команды категории", value="```/help, /avatar, /click, /clicks, /add_click, /remove_click, /addrole, /afk, /botinfo, /create_notes, /me_notes, /remove_notes, /msg, /new_nick, /numbergame, /partnerbot, /user.```")
            asyli.set_footer(text=f"Если каких то команды нету в хелпе пишите /report")
            await interaction.response.send_message(embed=asyli,ephemeral=True)

@client.slash_command(name = "help", description = "Инфо каманды")
async def help(ctx):
    asyli = discord.Embed(title="Список Команд в боте", color=0x0050ff)
    asyli.add_field(name="Модерация", value="```/ban, /editname, /slowmode, /kick, /warn, /unwarn, /antibot, /clear, /vote, /mute, /unmute, /rolemute, /unrolemute.```")
    asyli.add_field(name="Установки", value="```/set_emoji_economy, /set_log_channel, /set_appeal, /set_account, /set_ideas, /set_job.```")
    asyli.add_field(name="Экономика", value="```/work, /timely, /casino, /add_money, /remove_money, /balance, /shop, /buy, /create_item, /remove_item.```")
    asyli.add_field(name="Другие", value="```/help, /avatar, /click, /clicks, /add_click, /remove_click, /addrole, /afk, /botinfo, /create_notes, /me_notes, /remove_notes, /msg, /new_nick, /numbergame, /partnerbot, /user.```")
    asyli.set_footer(text=f"Если каких то команды нету в хелпе пишите /report")
    select = MenuOnHelp()
    view = View()
    view.add_item(select)
    await ctx.send(embed=asyli, view=view)

@client.slash_command(name="avatar", description="Показывает аватарку учасиника")
async def avatar(ctx, member: Option(discord.Member)):
    asyli = discord.Embed(title="Успешно!", description=f"Аватар: <@{member.id}>", color=0x0050ff)
    asyli.set_image(url=member.avatar.url)
    await ctx.send(embed=asyli)

@client.slash_command(name="mute", description="Выдать time-out участнику.")
@commands.has_permissions(kick_members = True)
async def mute(interaction: discord.MessageInteraction, member: discord.Member, *, reason, days: int = None, hours: int = None, minutes: int = None, seconds: int = None):
    logchannel = db.get(f"logchannel_{ctx.guild.id}") 
    if days == None:
        days = 0
    if hours == None:
        hours = 0 
    if minutes == None:
        minutes = 0
    if seconds == None:
        seconds = 0
    asyli = discord.Embed(title="Участник наказан", description=f"Выдан тайм-аут участнику: <@{member.id}>", color=0x0050ff)
    asyli.set_thumbnail(url=member.avatar.url)
    asyli.add_field(name="Модератор:", value=f"**<@{interaction.author.id}>**")
    asyli.add_field(name="Виновник:", value=f"**{member.mention}**")
    asyli.add_field(name="Причина:", value=f"`{reason}`")
    await interaction.response.send_message(embeds=[asyli])
    await member.timeout(until = discord.utils.utcnow() + datetime.timedelta (days=days, hours=hours, minutes=minutes, seconds=seconds), reason=reason)
    asyli = discord.Embed(title="Вы в мьюте!", description=f"**Модератор:** <@{interaction.author.id}>\n\n**Причина:**\n{reason}", color=0x0050ff)
    button = Button(label=f"Отправленно с {interaction.guild}", style=discord.ButtonStyle.blurple, emoji="📨", disabled=True)
    view = View()
    view.add_item(button)
    await member.send(embed=asyli, view=view)
    if logchannel == None:
        channel = await client.fetch_channel(1033387036209598554)
        asyli = discord.Embed(title = f"Канала нету", description = f"У вас нету канала для логов", color=0x0050ff)
        await channel.send(embed=asyli)
    else:
        channel = await client.fetch_channel(logchannel)
        asyli = discord.Embed(title = f"{member} был замьючен", description = f"Модератор: {ctx.author.name}\n В {datetime.datetime.now}", color=0x0050ff)
        await channel.send(embed=asyli)

@client.slash_command(name='unmute', description='РазМьют участника')
@commands.has_permissions(kick_members = True)
async def unmute(interaction: discord.MessageInteraction, member: discord.Member):
    asyli = discord.Embed(title="Участник больше не наказан", description=f"Тайм-аут участника: <@{member.id}> снят", color=0x0050ff)
    await interaction.response.send_message(embeds=[asyli])
    await member.remove_timeout()

@unmute.error
async def unmute_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

@client.slash_command(name="warn", description="Выдать предупреждение")
@commands.has_permissions(kick_members = True)
async def warn(ctx, member: Option(discord.Member), reason):
    db.add(f'warns_{ctx.guild.id}_{member.id}', 1) 
    warns = db.get(f"warns_{ctx.guild.id}_{member.id}")
    asyli = discord.Embed(title=f"Выдано предупреждение", color=0x0050ff)
    asyli.add_field(name="Случай:", value=f"№{warns}")
    asyli.add_field(name="Модератор:", value=f"**<@{ctx.author.id}>**")
    asyli.add_field(name="Виновник:", value=f"**{member.mention}**")
    asyli.add_field(name="Причина:", value=f"`{reason}`")
    await ctx.send(embed=asyli)
    asyli = discord.Embed(title="Предупреждение!", description=f"**Модераор:** <@{ctx.author.id}>\n\nВам выдано предупреждение с сервера **{ctx.guild}.**\n\nПричина: {reason}", color=0x0050ff)
    button = Button(label=f"Отправденно с {ctx.guild}", style=discord.ButtonStyle.blurple, emoji="<:mail:1033738336067657808>", disabled=True)
    view = View()
    view.add_item(button)
    await member.send(embed=asyli, view=view)

@warn.error
async def warn_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

@client.slash_command(name="warns", description="Твои преды")
async def warns(ctx, member: Option(discord.Member)):
   warns = db.get(f"warns_{ctx.guild.id}_{member.id}")
   if warns == None:
       warns = 0
       asyli = discord.Embed(title="Пусто", description=f"У <@{member.id}> нету предупреждений!", color=0x0050ff)
       await ctx.send(embed=asyli)
   else:
       asyli = discord.Embed(title="Предупреждения", description=f"<@{member.id}> замечено `№{warns}`случай!", color=0x0050ff)
       await ctx.send(embed=asyli)

@client.slash_command(name="unwarn", description="Снять предупреждение")
@commands.has_permissions(kick_members = True)
async def unwarn(ctx,member: Option(discord.Member)):
    warns = db.get(f"warns_{ctx.guild.id}_{member.id}")
    if int(warns) <= 0: return await ctx.send(asyli = discord.Embed(title="Откланено", description=f"У этого пользователя нету варнов", color=0x0050ff))
    db.subtract(f'warns_{ctx.guild.id}_{member.id}', 1)
    asyli = discord.Embed(title="Снятие преда", description=f"Участнику {member.mention} снято предупреждение", color=0x0050ff)
    await ctx.send(embed=asyli)

@unwarn.error
async def unwarn_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

class buttonklick(View):
   def __init__(self):
     super().__init__(timeout=None)

   @discord.ui.button(label="click", style=discord.ButtonStyle.blurple)
   async def click(self,button: discord.ui.Button,interaction: discord.Interaction):
       db.add(f'klick_{interaction.guild_id}_{interaction.user.id}', 1)
       clicks = db.get(f'klick_{interaction.guild_id}_{interaction.user.id}')
       asyli = discord.Embed(title="Жмите для клика", description=f"Ваши клики: {clicks}", color=0x0050ff)
       await interaction.response.edit_message(embed = asyli)

@client.slash_command(name="click", description="Кликать")
async def click(interaction: discord.Interaction):
    clicks = db.get(f'klick_{interaction.guild_id}_{interaction.user.id}')
    asyli = discord.Embed(title="Жмите для клика", description=f"Ваши клики: {clicks}", color=0x0050ff)
    await interaction.response.send_message(embed = asyli, view = buttonklick())

@client.slash_command(name="clicks", description="Сумма кликов")
async def clicks(ctx):
    click = db.get(f'klick_{ctx.guild.id}_{ctx.author.id}') 
    asyli = discord.Embed(title="Ваши клики", description=f"Ваши клики: {click}", color=0x0050ff)
    await ctx.response.send_message(embed=asyli, ephemeral=True)

@client.slash_command(name="remove_klick", description="Снять клики")
@commands.has_permissions(administrator = True)
async def remove_click(ctx, member: discord.Member, amount: int = None):
    if amount == None or amount <= 0:
        return await ctx.send(discord.Embed(title="Нельзя cнимать кол-во кликов меньше 0", color=0x0050ff))
    db.subtract(f'klick_{ctx.guild.id}_{member.id}', amount)
    asyli = discord.Embed(title="Вы сняли клики", description=f"Вы сняли {amount} кликов", color=0x0050ff)
    await ctx.response.send_message(embed=asyli)

@remove_click.error
async def remove_click_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

@client.slash_command(name="add_klick", description="Добавить клики")
@commands.has_permissions(administrator = True)
async def add_click(ctx, member: discord.Member, amount: int = None):
    if amount == None or amount <= 0:
        return await ctx.send(discord.Embed(title="Нельзя доволять кол-во кликов меньше 0", color=0x0050ff))
    db.add(f'klick_{ctx.guild.id}_{member.id}', amount)
    asyli = discord.Embed(title="Вы добавили клики", description=f"Вы добавили {amount} кликов", color=0x0050ff)
    await ctx.response.send_message(embed=asyli)

@add_click.error
async def add_click_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

class buttonadluck(View):
   def __init__(self,member,amount):
     super().__init__(timeout=None)

   #def disableButton(self):
      #self.payb.disabled = True
   
   @discord.ui.button(label="Ещё раз", style=discord.ButtonStyle.green)
   async def adluckb(button: discord.ui.Button,interaction: discord.Interaction):
       db.add(f"luck_{interaction.guild_id}_{interaction.user.id}", 1)
       luck = db.get(f"luck_{interaction.guild_id}_{interaction.user.id}")
       asyli=discord.Embed(title = f"Вы вииграли", description=f"У вас +{luck} удача", color=0x0050ff)
       #self.disableButton()
       await interaction.response.edit_message(embed=asyli)

class buttonremluck(View):
   def __init__(self,member,amount):
     super().__init__(timeout=None)

   #def disableButton(self):
      #self.rluckb.disabled = True

   @discord.ui.button(label="Ещё раз", style=discord.ButtonStyle.red)
   async def rluckb(button: discord.ui.Button,interaction: discord.Interaction):
       db.subtract(f"luck_{interaction.guild_id}_{interaction.user.id}", 1)
       luck = db.get(f"luck_{interaction.guild_id}_{interaction.user.id}")
       asyli=discord.Embed(title = f"Вы проиграли", description=f"У вас -{luck} удача", color=0x0050ff)
       #self.disableButton()
       await interaction.response.edit_message(embed = asyli)

class GameNumber(Select):
    def __init__(self) -> None:
        super().__init__(
            options=[
            discord.SelectOption(label="Профиль", description="Просмотреть свой результат"),
            discord.SelectOption(label="Бонус", description="Тут вы можете получить бесплатно билеты на игру"),
            discord.SelectOption(label="Начать", description="Начать играть"),
            discord.SelectOption(label="Документация", description="Посмотреть об игре удача")  
            ]
        )
    async def callback(self, interaction):
        if self.values[0] == "Профиль":
            luck = db.get(f"luck_{interaction.guild_id}_{interaction.user.id}")
            tiket = db.get(f"tiket_{interaction.guild_id}_{interaction.user.id}")
            if tiket == None:
                tiket = "0"
            if luck == None:
                luck = "0"
            asyli = discord.Embed(title="Ваш профиль", description=f"Ваша удача: {luck}\nВаши билеты: {tiket}", color=0x0050ff)
            await interaction.response.send_message(embed=asyli,ephemeral=True)
        if self.values[0] == "Бонус":
            db.add(f"tiket_{interaction.guild_id}_{interaction.user.id}", 10)
            luck = db.get(f"luck_{interaction.guild_id}_{interaction.user.id}")
            tiket = db.get(f"tiket_{interaction.guild_id}_{interaction.user.id}")
            if tiket == None:
                tiket = "0"
            if luck == None:
                luck = "0"
            asyli = discord.Embed(title="Ваш бонус", description=f"Билеты: {tiket}(+10)", color=0x0050ff)
            await interaction.response.send_message(embed=asyli,ephemeral=True)
        if self.values[0] == "Начать":
            luck = db.get(f"luck_{interaction.guild_id}_{interaction.user.id}")
            tiket = db.get(f"tiket_{interaction.guild_id}_{interaction.user.id}")
            if tiket == None:
                tiket = "0"
                asyli = discord.Embed(title="Игра не работает", description=f"Вы не можете играть так как у вас нету билетов", color=0x0050ff)
                await interaction.response.send_message(embed=asyli,ephemeral=True)
            if luck == None:
                luck = "0"
            asyli = discord.Embed(title="Играть", description=f"Начните что бы играть", color=0x0050ff)
            game = random.choice(['buttonremluck', 'buttonadluck'])
            await interaction.response.send_message(embed=asyli,ephemeral=True, view=game)
        if self.values[0] == "Документация":
            luck = db.get(f"luck_{interaction.guild_id}_{interaction.user.id}")
            tiket = db.get(f"tiket_{interaction.guild_id}_{interaction.user.id}")
            asyli = discord.Embed(title="Документация", color=0x0050ff)
            asyli.add_field(name='Сколько балов дают?', value=f'Вначале вам даётся 15 билетов, позже вам нужно брать билеты в кнопке Бонус')
            asyli.add_field(name='Зачем нужны билеты?', value = f'Билеты это доступ к испытании удачи, каждая попытка отнимает 1 билет, при выграше вам дадут 1 очко под названием "Удача"')
            asyli.add_field(name='Какие шансы победить?', value = f'Шансы равны (50/50)')
            await interaction.response.send_message(embed=asyli,ephemeral=True)

@client.slash_command(name="luck", description="Добавить заметку")
async def luck(ctx):
    tiket = db.get(f"tiket_{ctx.guild.id}_{ctx.author.id}")
    if tiket == None:
        tiket = "0"
    asyli = discord.Embed(title="Игра на удачу", description=f"Ваши былеты: {tiket}", color=0x0050ff)
    select = GameNumber()
    view = View()
    view.add_item(select)
    await ctx.response.send_message(embed=asyli, ephemeral=True, view=view)

@client.slash_command(name="create_notes", description="Добавить заметку")
async def notes(ctx, text: str):
    vip = db.get(f'vip_{ctx.guild.id}')
    if vip == None:
        asyli = discord.Embed(title="Как так?", description = f"Это вип команда.\nЕсли вы хотите вип на вашем серевере свяжитесь с `MVXXL#9919`", color = 0x0050ff)
        asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299204393836625/free-icon-danger-5885380-removebg-preview.png")
        await ctx.send(embed=asyli)
    else:
        db.set(f'text_{ctx.guild.id}_{ctx.author.id}', str(text))
        asyli = discord.Embed(title="Вы добавили свою заметку", description=f"Заметка:\n{text}", color=0x0050ff)
        await ctx.response.send_message(embed=asyli, ephemeral=True)

@client.slash_command(name="me_notes", description="Просмотреть свою заметку")
async def me_notes(ctx):
    vip = db.get(f'vip_{ctx.guild.id}')
    if vip == None:
        asyli = discord.Embed(title="Как так?", description = f"Это вип команда.\nЕсли вы хотите вип на вашем серевере свяжитесь с `MVXXL#9919`", color = 0x0050ff)
        asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299204393836625/free-icon-danger-5885380-removebg-preview.png")
        await ctx.send(embed=asyli)
    else:
        text = db.get(f'text_{ctx.guild.id}_{ctx.author.id}')
        if text == None:
            asyli = discord.Embed(title="У вас нету заметок",color=0x0050ff)
            await ctx.response.send_message(embed=asyli, ephemeral=True)
        asyli = discord.Embed(title="Ваши заметки", description=f"Заметка:\n{text}", color=0x0050ff)
        await ctx.response.send_message(embed=asyli, ephemeral=True)

@client.slash_command(name="remove_notes", description="Просмотреть свою заметку")
async def remove_notes(ctx):
    vip = db.get(f'vip_{ctx.guild.id}')
    if vip == None:
        asyli = discord.Embed(title="Как так?", description = f"Это вип команда.\nЕсли вы хотите вип на вашем серевере свяжитесь с `MVXXL#9919`", color = 0x0050ff)
        asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299204393836625/free-icon-danger-5885380-removebg-preview.png")
        await ctx.send(embed=asyli)
    else:
        db.delete(f'text_{ctx.guild.id}_{ctx.author.id}')
        text = db.get(f'text_{ctx.guild.id}_{ctx.author.id}')
        asyli = discord.Embed(title="Вы сняли свою заметку", description=f"Заметка:\n{text}", color=0x0050ff)
        await ctx.response.send_message(embed=asyli, ephemeral=True)

@client.slash_command(name="antibot", description="Кикнуть всех неверифицированных ботов")
@commands.has_permissions(administrator = True)
async def antibot(ctx):
   current = db.get(f'antibot_{ctx.guild.id}')
   if current == None:
      db.set(f'antibot_{ctx.guild.id}', 'on')
      asyli = discord.Embed(title="Авто модерация вкл", description=f"Теперь я буду кикать всех не верифицированных ботов!", color=0x0050ff)
      await ctx.send(embed=asyli)
   else:
      db.delete(f'antibot_{ctx.guild.id}')
      asyli = discord.Embed(title="Авто модерация викл", description=f"Я больше не кикаю не верифицированных ботов", color=0x0050ff)
      await ctx.send(embed=asyli)

@antibot.error
async def antibot_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

@client.slash_command(name="antilinks", description="Мутить всех за ссылк")
@commands.has_permissions(administrator = True)
async def antilinks(ctx):
   current = db.get(f'antilinks_{ctx.guild.id}')
   guild = ctx.guild
   mutedRole = discord.utils.get(guild.roles, name="As-muted")
   if not mutedRole:
       mutedRole = await guild.create_role(name="As-muted")
       for channel in guild.channels:
           await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
   if current == None:
       db.set(f'antilinks_{ctx.guild.id}', 'on')
       asyli = discord.Embed(title="Авто модерация вкл", description=f"Теперь я буду мутить всех (кроме админов) за ссылк дискорда", color=0x0050ff)
       await ctx.send(embed=asyli)
   else:
       db.delete(f'antilinks_{ctx.guild.id}')
       asyli = discord.Embed(title="Авто модерация викл", description=f"Я больше не буду мутить всех (кроме админов) за ссылк дискорда", color=0x0050ff)
       await ctx.send(embed=asyli)

@antilinks.error
async def antilinks_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

@client.slash_command(name="rolemute", description="Мьют")
@commands.has_permissions(administrator = True)
async def asmute(ctx, member: discord.Member, reason="Не указана"):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="As-muted")
    if not mutedRole:
        mutedRole = await guild.create_role(name="As-muted")
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    asyli = discord.Embed(title="Модерация", description=f"Участнику: {member.mention} было выдано наказание ввиде мута", color=0x0050ff)
    asyli.add_field(name="Причина:", value=reason, inline=False)
    await ctx.send(embed=asyli)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" Вам выдали мут на сервере: {guild.name}, Причина: {reason}")

@asmute.error
async def asmute_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

@client.slash_command(name="unrolemute", description="Снять мьют")
@commands.has_permissions(manage_messages=True, kick_members=True)
async def unrolemute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
   await member.remove_roles(mutedRole)
   asyli = discord.Embed(title="Модерация", description=f" С участника: {member.mention} Сняты все наказания", color=0x0050ff)
   await member.send(f"С вас была снята блокировка чата на сервере: {ctx.guild.name}")
   await ctx.send(embed=asyli)

@unrolemute.error
async def unrolemute_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

@client.slash_command(name="addrole", description="Добавить роль")
@commands.has_permissions(administrator = True)
async def addrole(ctx, member: discord.Member = None, role: discord.Role = None, guild: discord.Guild = None):
    guild = ctx.guild if not guild else guild
    asyli = discord.Embed(title='Роль выдана', color=0x0050ff)
    await ctx.channel.purge(limit = 1)
    await member.add_roles(role)
    asyli.set_thumbnail( url=member.avatar.url)
    asyli.add_field(name='Модератор', value=f'{ctx.author.mention}')
    asyli.add_field( name = 'Пользователь', value = f'{member.mention}')
    asyli.add_field( name = 'Роль', value = f'{role.mention}')
    await ctx.send(embed=asyli, delete_after=15)

@addrole.error
async def addrole_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)     

@client.slash_command(name="user", description="Инфо о участнике")
async def user(ctx, member: Option(discord.Member) = None):
    if member == None:
        member = ctx.author
    if str(member.status) == 'dnd': status = '⛔Не беспокоить'
    if str(member.status) == 'idle': status = '🌙Отошёл'
    if str(member.status) == 'invisible': status = '🖤Неведимка'
    if str(member.status) == 'online': status = '💚Онлайн'
    if str(member.status) == 'offline': status = '🖤Офлайн'    
    created = int(time.mktime(member.created_at.timetuple()))
    joined = int(time.mktime(member.joined_at.timetuple()))
    roles = [role for role in member.roles]
    asyli = discord.Embed(color=0x0050ff, title=f"Инфо о - {member}")
    asyli.set_thumbnail(url=member.avatar.url)
    asyli.set_footer(text=f"Вызвал: {ctx.author}")
    asyli.add_field(name="ID:", value=member.id)
    asyli.add_field(name="Имя:", value=member.display_name)
    asyli.add_field(name="Статус", value=f"{status}")
    asyli.add_field(name="Создал(а) аккаунт в:", value=f"<t:{created}>")
    asyli.add_field(name="Зашёл(ла) на сервер в:", value=f"<t:{joined}>")
    asyli.add_field(name="Высшая роль:", value=member.top_role.mention)
    await ctx.send(embed=asyli)

@client.slash_command(name="clear", description="Очистить чат")
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount: int):
    if amount <=0:
        asyli = discord.Embed(title = 'Ошибка.', description='Нельзя очистить меньше нуля. Ваше значение: {}'.format(amount), color = 0xe800ff)
    else:
        message=await ctx.channel.purge(limit=amount)
        asyli = discord.Embed(title = 'Очистка', description=f'{ctx.author.mention} очистил {amount} сообщений.', color = 0xe800f)
        await ctx.send(embed=asyli, delete_after=5)

@client.slash_command(name="set_log_channel", description="Установить канал для логов")
@commands.has_permissions(manage_messages = True)
async def set_log_channel(ctx, channel: discord.TextChannel):
    vip = db.get(f'vip_{ctx.guild.id}')
    if vip == None:
        asyli = discord.Embed(title="Как так?", description = f"Это вип команда.\nЕсли вы хотите вип на вашем серевере свяжитесь с `MVXXL#9919`", color = 0x0050ff)
        asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299204393836625/free-icon-danger-5885380-removebg-preview.png")
        await ctx.send(embed=asyli)
    else:
        db.set(f"logchannel_{ctx.guild.id}", int(channel.id))
        asyli = discord.Embed(title = "Установка канала для логов", description = f"Вы успешно установили канал <#{channel.id}> в качестве канала для логов!", color=0x0050ff)
        await ctx.send(embed=asyli)

class buttonpartner(View):
   def __init__(self, namebot):
     super().__init__(timeout=None)
     self.namebot = namebot

   def disableButton(self):
      self.yespart.disabled = True
      self.nopart.disabled = True

   @discord.ui.button(label="Да", style=discord.ButtonStyle.green)
   async def yespart(self,button: discord.ui.Button,interaction: discord.Interaction):
       channel = client.get_channel(1037810824691068978)
       asyli=discord.Embed(title = f"Cпасибо ваша заявка отправлена", description=f"Сервер поддержки: https://discord.gg/st5uPyADyC", color=0x0050ff)
       self.disableButton()
       await interaction.response.edit_message(embed=asyli, view =self)
       asyli=discord.Embed(title = f"Зявка на бота", description=f"Ник бота: {self.namebot}\nУсловия приняты!", color=0x0050ff)
       await channel.send(embed=asyli)

   @discord.ui.button(label="Нет", style=discord.ButtonStyle.red)
   async def nopart(self,button: discord.ui.Button,interaction: discord.Interaction):
       channel = client.get_channel(1037810824691068978)
       asyli=discord.Embed(title = f"Откланено", description=f"Вы отказали в наших условиях", color=0x0050ff)
       self.disableButton()
       await interaction.response.edit_message(embed = asyli, view = self)
       asyli=discord.Embed(title = f"Зявка на бота", description=f"Ник бота: {self.namebot}\nУсловия неприняты!", color=0x0050ff)
       await channel.send(embed=asyli)

@client.slash_command(name="partnerbot", description="Cоглашение на партнерство ботов")
async def partnerbot(ctx, namebot: str):
    asyli = discord.Embed(title = "Наши условия", description = f"Вы соглашаетесь что ваш бот не принисёт никакого вреда нашему серверу\n\nА также наш бот должен быть выше обычных участниов", color=0x0050ff)
    await ctx.send(embed=asyli, view = buttonpartner(namebot))

@client.slash_command(name="remove_log_channel", description="Снять канал для логов")
@commands.has_permissions(manage_messages = True)
async def remove_log_channel(ctx):
    vip = db.get(f'vip_{ctx.guild.id}')
    if vip == None:
        asyli = discord.Embed(title="Как так?", description = f"Это вип команда.\nЕсли вы хотите вип на вашем серевере свяжитесь с `MVXXL#9919`", color = 0x0050ff)
        asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299204393836625/free-icon-danger-5885380-removebg-preview.png")
        await ctx.send(embed=asyli)
    else:
        db.delete(f"logchannel_{ctx.guild.id}")
        channel = db.get(f"logchannel_{ctx.guild.id}")
        if channel == None:
            channel = "Отсуствует"
            asyli = discord.Embed(title = "Ошибка", description = f"У вас не установлен канал для логов что бы удалить из", color=0x0050ff)
            await ctx.send(embed=asyli)
        asyli = discord.Embed(title = "Удаиление канала для логов", description = f"Вы успешно удалили канал <#{channel.id}>", color=0x0050ff)
        await ctx.send(embed=asyli)

@client.slash_command(name="my_log_channel", description="Проверить канал для логов на сервере")
async def my_log_channel(ctx):
    vip = db.get(f'vip_{ctx.guild.id}')
    if vip == None:
        asyli = discord.Embed(title="Как так?", description = f"Это вип команда.\nЕсли вы хотите вип на вашем серевере свяжитесь с `MVXXL#9919`", color = 0x0050ff)
        asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299204393836625/free-icon-danger-5885380-removebg-preview.png")
        await ctx.send(embed=asyli)
    else:
        channel = db.get(f"logchannel_{ctx.guild.id}")
        if channel == None:
            channel = "Отсуствует"
            asyli = discord.Embed(title = "Ошибка", description = f"У вас не установлен канал для логов", color=0x0050ff)
            await ctx.send(embed=asyli)
        asyli = discord.Embed(title = "Канал для логов", description = f"Ваш канал для логов: <#{channel}>", color=0x0050ff)
        await ctx.send(embed=asyli)

@client.slash_command(name="add_money", description="Прибавить себе деняг")
@commands.has_permissions(administrator = True)
async def add_money(ctx, member: discord.Member, amount: int):
   emoji = db.get(f'emoji_{ctx.guild.id}')
   db.add(f"money_{ctx.guild.id}_{member.id}", amount)
   if amount == None or amount <= 0:
        return await ctx.send(discord.Embed(title="Нельзя запрашивать кол-во деняг меньше 0", color=0x0050ff))
   if emoji == None:
       emoji = "🪙" 
       asyli = discord.Embed(title="Деньги пришли", description=f"Вы добавили себе {amount}{emoji} деняг", color=0x0050ff)
       await ctx.send(embed=asyli)
   else:
       asyli = discord.Embed(title="Деньги пришли", description=f"Вы добавили себе {amount}{emoji} деняг", color=0x0050ff)
       await ctx.send(embed=asyli)

@add_money.error
async def add_money_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

@client.slash_command(name="casino", description="Сиграть в казино")
async def casino(ctx, bet: int):
    emoji = db.get(f'emoji_{ctx.guild.id}')
    money = db.get(f"money_{ctx.guild.id}_{ctx.author.id}")
    d = random.choice([ 253, 107, 103, 666, 777])
    if money == None or int(money)<bet:
       if money == None:
           db.set(f"money_{interaction.guild_id}_{interaction.author.id}",0)
       asyli = discord.Embed(title="Ошибка", description=f"У вас надостаточно средств для игры", color=0x0050ff)
       await ctx.send(embed=asyli)
    else:
       if emoji == None:
           emoji = "🪙"
       if d == 777 or d == 666:
          db.add(f"money_{ctx.guild.id}_{ctx.author.id}", bet)
          asyli = discord.Embed(title="Победа", description=f"Вы победили в казино\nСтавка: {bet}{emoji}", color=0x0050ff)
          await ctx.send(embed=asyli)
       else:
          db.subtract(f"money_{ctx.guild.id}_{ctx.author.id}", bet)
          asyli = discord.Embed(title="Проиграш", description=f"Вы проиграли в казино\nСтавка: {bet}{emoji}", color=0x0050ff)
          await ctx.send(embed=asyli)

@client.slash_command(name="work", description="Работать")
@commands.cooldown(1, 300, commands.BucketType.user)
async def work(ctx):
   emoji = db.get(f'emoji_{ctx.guild.id}')
   r = random.randint(50, 3000)
   db.add(f'money_{ctx.guild.id}_{ctx.author.id}', r)
   if emoji == None:
       emoji = "🪙"
       asyli = discord.Embed(title="Деньги пришли", description=f"Зарплата {r}{emoji} деняг", color=0x0050ff)
       await ctx.send(embed=asyli)
   else:
       asyli = discord.Embed(title="Деньги пришли", description=f"Зарплата {r}{emoji} деняг", color=0x0050ff)
       await ctx.send(embed=asyli)

@work.error
async def work_error(ctx, error):
     if isinstance(error, commands.CommandOnCooldown):
        asyli = discord.Embed(title="Ошибка!", description=f"Вы сможете использовать команду через `{error.retry_after:.2f}`", color=0x0050ff)
        await ctx.response.send_message(embed=asyli, ephemeral=True)

@client.slash_command(name="timely", description="Заработать деньги за 12ч")
@commands.cooldown(1, 43200, commands.BucketType.user)
async def timely(ctx):
   emoji = db.get(f'emoji_{ctx.guild.id}')
   db.add(f'money_{ctx.guild.id}_{ctx.author.id}', 1000)
   if emoji == None:
       emoji = "🪙"
       asyli = discord.Embed(title="Деньги пришли", description=f"Ваши деньги добавились 1000{emoji} деняг", color=0x0050ff)
       await ctx.send(embed=asyli)
   else:
       asyli = discord.Embed(title="Деньги пришли", description=f"Ваши деньги добавились 1000{emoji} деняг", color=0x0050ff)
       await ctx.send(embed=asyli)

@timely.error
async def work_error(ctx, error):
     if isinstance(error, commands.CommandOnCooldown):
        asyli = discord.Embed(title="Ошибка!", description=f"Вы сможете использовать команду через `{error.retry_after:.2f}`", color=0x0050ff)
        await ctx.response.send_message(embed=asyli, ephemeral=True)

@client.slash_command(name="balance", description="Баланс участника")
async def balance(ctx, member: discord.Member):
   emoji = db.get(f'emoji_{ctx.guild.id}')
   money = db.get(f"money_{ctx.guild.id}_{member.id}")
   if money == None:
       money = 0
   if emoji == None:
       emoji = "🪙" 
       asyli = discord.Embed(description=f"На счету: {money}{emoji}", color=0x0050ff)
       asyli.set_author(name=f"{member}", icon_url=member.avatar.url)
       asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299201160040508/free-icon-baht-6506237-removebg-preview.png")
       asyli.set_footer(text="/add_money <сумма> - чтобы пополнить валюту.")
       await ctx.send(embed=asyli)  
   else:
       asyli = discord.Embed(description=f"На счету: {money}{emoji}", color=0x0050ff)
       asyli.set_author(name=f"{member}", icon_url=member.avatar.url,)
       asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299201160040508/free-icon-baht-6506237-removebg-preview.png")
       asyli.set_footer(text="/add_money <сумма> - чтобы пополнить валюту.")
       await ctx.send(embed=asyli) 

class buttontrans(View):
   def __init__(self,clicks):
     super().__init__(timeout=None)
     self.clicks = clicks

   def disableButton(self):
      self.translationb.disabled = True
      self.notranslationb.disabled = True

   @discord.ui.button(label="Потвердить", style=discord.ButtonStyle.green)
   async def translationb(self,button: discord.ui.Button,interaction: discord.Interaction):
       db.subtract(f"klick_{interaction.guild_id}_{interaction.user.id}", self.clicks)
       db.add(f"money_{interaction.guild_id}_{interaction.user.id}", self.clicks)
       asyli=discord.Embed(title = f"Перевод", description=f"Вы перевели клики в деньги", color=0x0050ff)
       self.disableButton()
       await interaction.response.edit_message(embed=asyli, view=self)

   @discord.ui.button(label="Отменить", style=discord.ButtonStyle.red)
   async def notranslationb(self,button: discord.ui.Button,interaction: discord.Interaction):
       asyli=discord.Embed(title = f"Откланено", description=f"Вы отклонили перевод не удался, вы отклонили операцию", color=0x0050ff)
       self.disableButton()
       await interaction.response.edit_message(embed = asyli, view = self)

@client.slash_command(name="translation", description="Перевести клики в деньги")
async def translation(interaction: discord.Interaction, clicks: int):
    emoji = db.get(f'emoji_{interaction.guild_id}')
    click = db.get(f'klick_{interaction.guild_id}_{interaction.user.id}')
    if emoji == None:
        emoji = "🪙"
    if click == None or int(click)<clicks:
       if click == None:
           db.set(f"klick_{interaction.guild_id}_{interaction.user.id}",0)
       asyli = discord.Embed(title="Ошибка!", description=f"У вас нету столько сколько вы указали!", color=0x0050ff)
       await interaction.response.send_message(embed=asyli)
    else:         
        asyli = discord.Embed(title="Перевод кликов", description=f"Ваши клики: {click}\nПеревести деньги с потверждением с низу", color=0x0050ff)
        await interaction.response.send_message(embed=asyli, view=buttontrans(clicks))

@client.slash_command(name="leaderboard_money", description="Таблица лидеров экономики")
async def leaderboard_money(ctx):
    emoji = db.get(f'emoji_{ctx.guild.id}')
    if emoji == None:
        emoji = "🪙"
    leaders = []
    srt = list(filter(lambda a: f'money_{ctx.guild.id}' in a[0], db.all()))
    if len(srt) == 0: return
    for i in srt:
        leaders.append({
            'money': int(i[1]),
            'id': int(i[0].split('_')[2])
        })
    leaders.sort(key = lambda a: a['money'], reverse = True)
    emb = discord.Embed(title = 'Лидеры', color=0x0050ff)
    for i in leaders:
        user = client.get_user(i['id'])
        emb.add_field(name = user, value = i['money'f"{emoji}"])
    await ctx.send(embed = emb)

@client.slash_command(name="leaderboard_click", description="Таблица лидеров по кликам")
async def leaderboard_click(ctx):
    leaders = []
    srt = list(filter(lambda a: f'klick_{ctx.guild.id}' in a[0], db.all()))
    if len(srt) == 0: return
    for i in srt:
        leaders.append({
            'klick': int(i[1]),
            'id': int(i[0].split('_')[2])
        })
    leaders.sort(key = lambda a: a['klick'], reverse = True)
    emb = discord.Embed(title = 'Лидеры', color=0x0050ff)
    for i in leaders:
        user = client.get_user(i['id'])
        emb.add_field(name = user, value = i['klick'])
    await ctx.send(embed = emb)

@client.slash_command(name="remove_money", description="Очистить деньги участника")
@commands.has_permissions(administrator = True)
async def remove_money(ctx, member: discord.Member = None, amount: int = None):
   emoji = db.get(f'emoji_{ctx.guild.id}')
   if amount == None or amount <= 0:
      return await ctx.send(discord.Embed(title="Нельзя запрашивать кол-во деняг меньше 0", color=0x0050ff))
   if member == None:
       member = ctx.author.id
       if emoji == None:
           emoji = "🪙"
           db.add(f"money_{ctx.guild.id}_{ctx.author.id}", amount)
           asyli = discord.Embed(title="Деньги ушли", description=f"Вы сняли себе {amount}{emoji} деняг", color=0x0050ff)
           await ctx.send(embed=asyli)
       else:
            db.add(f"money_{ctx.guild.id}_{ctx.author.id}", amount)
            asyli = discord.Embed(title="Деньги ушли", description=f"Вы сняли себе {amount}{emoji} деняг", color=0x0050ff)
            await ctx.send(embed=asyli)
   else:
       if emoji == None:
           emoji = "🪙"
           db.add(f"money_{ctx.guild.id}_{member.id}", amount)
           asyli = discord.Embed(title="Деньги ушли", description=f"Вы сняли у {member.mention} {amount}{emoji} деняг", color=0x0050ff)
           await ctx.send(embed=asyli)
       else:
           db.add(f"money_{ctx.guild.id}_{member.id}", amount)
           asyli = discord.Embed(title="Деньги ушли", description=f"Вы сняли у {member.mention} {amount}{emoji} деняг", color=0x0050ff)
           await ctx.send(embed=asyli)

@remove_money.error
async def remove_money_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

class buttonpay(View):
   def __init__(self,member,amount):
     super().__init__(timeout=None)
     self.member = member
     self.amount = amount

   def disableButton(self):
      self.payb.disabled = True
      self.nopayb.disabled = True

   @discord.ui.button(label="Потвердить", style=discord.ButtonStyle.green)
   async def payb(self,button: discord.ui.Button,interaction: discord.Interaction):
       db.subtract(f"money_{interaction.guild_id}_{interaction.user.id}", self.amount)
       db.add(f"money_{interaction.guild_id}_{self.member.id}", self.amount)
       asyli=discord.Embed(title = f"Передача средств", description=f"Вы передали деньги ", color=0x0050ff)
       asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299201835311154/free-icon-gift-4585502-removebg-preview.png",)
       self.disableButton()
       await interaction.response.edit_message(embed=asyli, view =self)

   @discord.ui.button(label="Отменить", style=discord.ButtonStyle.red)
   async def nopayb(self,button: discord.ui.Button,interaction: discord.Interaction):
       asyli=discord.Embed(title = f"Откланено", description=f"Вы отклонили передачу средств", color=0x0050ff)
       self.disableButton()
       await interaction.response.edit_message(embed = asyli, view = self)

@client.slash_command(name="pay", description="Передать кол-во деняг")
async def pay(interaction: discord.Interaction, member: discord.Member, amount: int):
    money = db.get(f"money_{interaction.guild_id}_{interaction.author.id}")
    emoji = db.get(f'emoji_{interaction.guild.id}')
    if money == None or int(money)<amount:
        if money == None:
            db.set(f"money_{interaction.guild_id}_{interaction.author.id}",0)
        asyli = discord.Embed(title = f"У вас недстаточно средств!", description=f"Указано:{amount}\nЕсть:{money}", color=0x0050ff)
        await interaction.response.send_message(embed=asyli)
    else:
        if emoji == None:
            emoji = "🪙"
            asyli=discord.Embed(title = f"Передача средств",description=f"Потвердите операцию на передачу **{amount}**{emoji} полдьзователю {member.mention}", color=0x0050ff)
            await interaction.response.send_message(embed = asyli, view = buttonpay(member,amount))
        else:
            asyli=discord.Embed(title = f"Передача средств",description=f"Потвердите операцию на передачу **{amount}**{emoji} полдьзователю {member.mention}", color=0x0050ff)
            await interaction.response.send_message(embed = asyli, view = buttonpay(member,amount))
    
#@client.slash_command(name="add_stat", description="Чёто ничего...")
#@option("stat", description="Choose your gender", choices=["hp", "damage", "defence","speed","krit","luck"])
#async def add_stat(self, interaction: discord.Interaction, id: str, stat: str, value: int):
#    asyli=discord.Embed(title = f"тест",description=f"тест", color=0x0050ff)
#    await interaction.response.send_message(embed = asyli)

    #db.subtract(f"money_{ctx.author.id}", amount)
    #db.add(f"money_{member.id}", amount)

#@client.slash_command(name="click", description="Кликать")
#async def click(interaction: discord.Interaction):
#    clicks = db.get(f'klick_{interaction.guild_id}_{interaction.user.id}')
#    asyli = discord.Embed(title="Жмите для клика", description=f"Ваши клики: {clicks}", color=0x0050ff)
#    await interaction.response.send_message(embed = asyli, view = buttonklick())

@client.slash_command(name="new_nick", description="Изменить никнейм")
@commands.has_permissions(administrator=True)
async def new_nick(ctx, member: discord.Member, nickname):
    await ctx.send(embed=discord.Embed(title = f"Измениение ника!",description = f"Вы измениле никнейм на: {nickname}"))
    await member.edit(nick=nickname)

@client.slash_command(name="set_vip", description="Установить вип")
async def set_vip(ctx, guild: str):
    vip = db.get(f'vip_{ctx.guild.id}')
    if ctx.author.id == 606371934170513428:
        if vip == None:
            db.set(f'vip_{ctx.guild.id}', guild)
            asyli = discord.Embed(title="Установка випа", description=f"Вип активирован на сервере `{ctx.guild.name}`", color=0x0050ff)
            await ctx.send(embed=asyli)
            channel = await client.fetch_channel(1040323927169323131)
            asyli = discord.Embed(title="Установлен вип", description=f"{ctx.author.name} активировал вип на сервере `{ctx.guild.name}`", color=0x0050ff)
            await channel.send(embed=asyli)
        else:
            asyli = discord.Embed(title="Ошибка", description=f"Вы уже устанавливали вип на этом сервере!", color=0x0050ff)
            asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299204393836625/free-icon-danger-5885380-removebg-preview.png")
            await ctx.send(embed=asyli)
    else:
        asyli = discord.Embed(title="Ошибка", description=f"Вы не можете активировать вип так как только создатель бота может это сделать!", color=0x0050ff)
        asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299204393836625/free-icon-danger-5885380-removebg-preview.png")
        await ctx.send(embed=asyli)

@client.slash_command(name="delete_vip", description="Удалить вип")
async def delete_vip(ctx):
    vip = db.get(f'vip_{ctx.guild.id}')
    if ctx.author.id == 606371934170513428:
        if vip == None:
            asyli = discord.Embed(title="Ошибка", description=f"Вы уже устанавливали вип на этом сервере!", color=0x0050ff)
            asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299204393836625/free-icon-danger-5885380-removebg-preview.png")
            await ctx.send(embed=asyli)
        else:
            db.delete(f'vip_{ctx.guild.id}')
            asyli = discord.Embed(title="Удаление випа", description=f"Вип удалён на сервере `{ctx.guild.name}`", color=0x0050ff)
            asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299202703523880/free-icon-moon-4584520-removebg-preview.png",)
            await ctx.send(embed=asyli)
    else:
        asyli = discord.Embed(title="Ошибка", description=f"Вы не можете удалить вип так как только создатель бота может это сделать!", color=0x0050ff)
        asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299204393836625/free-icon-danger-5885380-removebg-preview.png",)
        await ctx.send(embed=asyli)

@client.slash_command(name="vip", description="Проверить вип")
async def vip(ctx):
    vip = db.get(f'vip_{ctx.guild.id}')
    if vip == None: 
        asyli = discord.Embed(title="Наличие випа", description=f"Ваш сервер `{ctx.guild.name}` не имеет вип", color=0x0050ff)
        asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299202703523880/free-icon-moon-4584520-removebg-preview.png",)
        asyli.set_footer(text='Стоимасть випа: 50Руб/25грн')
        button = Button(label="Оплатить", url="https://donatello.to/asyli", emoji="🇺🇦")
        button1 = Button(label="Оплатить", url="https://www.donationalerts.com/r/mvxxl", emoji="🇷🇺")
        
        view = View()
        view.add_item(button)
        view.add_item(button1)
        await ctx.send(embed=asyli, view=view)
    else:
        asyli = discord.Embed(title="Наличие випа", description=f"Ваш сервер `{ctx.guild.name}` уже имеет вип", color=0x0050ff)
        asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299202703523880/free-icon-moon-4584520-removebg-preview.png",)
        await ctx.send(embed=asyli)

@client.slash_command(name="shop", description="Магазин економики")
async def shop(ctx):
    emoji = db.get(f'emoji_{ctx.guild.id}')
    all_items = list(filter(lambda a: f'items_{ctx.guild.id}' in a[0], db.all()))
    emb = discord.Embed(title = 'Магазин', color=0x0050ff)
    if len(all_items) == 0:
        emb.description = 'Нету предметов'
        return await ctx.send(embed = emb)
    for i in all_items:
        if emoji == None:
            emoji = "🪙"
            emb.add_field(name = i[0].split('_')[2], value = f'{i[1]} {emoji}')
        else:
            emb.add_field(name = i[0].split('_')[2], value = f'{i[1]} {emoji}')
        
    await ctx.send(embed = emb)
    
@client.slash_command(name="buy", description="Купить придмет из магазина")
async def buy(ctx, item, amount = 1):
    itemm = db.get(f'items_{ctx.guild.id}_{item}')
    money = db.get(f'money_{ctx.guild.id}_{ctx.author.id}')
    if itemm == None: return await ctx.send(discord.Embed(title="Ошибка!", description=f"Такого придмета не существует!", color=0x0050ff))
    if int(money) == None or int(money) < int(itemm) * int(amount):
        return await ctx.send(discord.Embed(title="Ошибка!", description=f"У вас недостаточно средств", color=0x0050ff))
    if db.get(f'inventory_{ctx.guild.id}_{ctx.author.id}_{item}') == None:
        db.set(f'inventory_{ctx.guild.id}_{ctx.author.id}_{item}', amount)
    else:
        db.add(f'inventory_{ctx.guild.id}_{ctx.author.id}_{item}', int(amount))
        db.subtract(f'money_{ctx.guild.id}_{ctx.author.id}', int(itemm) * int(amount))
        asyli = discord.Embed(title="Покупка", description=f"Куплен предмет {item} `x{amount}`", color=0x0050ff)
        asyli.set_thumbnail(url="https://media.discordapp.net/attachments/1027899553606795325/1040299202217005076/free-icon-cart-4585350__1_-removebg-preview.png",)
        await ctx.send(embed=asyli)

@client.slash_command(name="set_emoji_economy", description="Установить емоджи экономике")
@commands.has_permissions(administrator = True)
async def set_emoji_economy(ctx, emoji: str):
    db.set(f'emoji_{ctx.guild.id}', emoji)
    emoji = db.get(f'emoji_{ctx.guild.id}')
    asyli = discord.Embed(title="Установка емоджи", description=f"Вы установили емоджи экономики: {emoji}", color=0x0050ff)
    await ctx.send(embed=asyli)

@set_emoji_economy.error
async def set_emoji_economy_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

@client.slash_command(name="delete_emoji_economy", description="Удалить емоджи экономике")
@commands.has_permissions(administrator = True)
async def delete_emoji_economy(ctx):
    db.delete(f'emoji_{ctx.guild.id}')
    emoji = db.get(f'emoji_{ctx.guild.id}')
    if emoji == None:
        emoji = "🪙"
        asyli = discord.Embed(title="Удаление емоджи", description=f"Вы удалили емоджи экономики\nЕмоджи по умочании: {emoji}", color=0x0050ff)
        await ctx.send(embed=asyli)

@delete_emoji_economy.error
async def delete_emoji_economy_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

@client.slash_command(name="inventory", description="Инвентарь экономики")
async def inventory(ctx):
    all_items = list(filter(lambda a: f'inventory_{ctx.guild.id}_{ctx.author.id}' in a[0], db.all()))
    emb = discord.Embed(title = 'Инвентарь', color=0x0050ff)
    if len(all_items) == 0:
        emb.description = 'Нету предметов'
        return await ctx.send(embed = emb)
    for i in all_items:
        emb.add_field(name = i[0].split('_')[3], value = f'x{i[1]}')
    
    await ctx.send(embed = emb)

@client.slash_command(name="create_item", description="Создать придмет в магазине")
@commands.has_permissions(administrator = True)
async def create_item(ctx, item, cost):
    if db.get(f'items_{ctx.guild.id}_{item}') != None:
        return await ctx.send(discord.Embed(title="Ошибка!", description=f"Такой предмет уже существует в магазине, выберите другое название", color=0x0050ff))
    db.set(f'items_{ctx.guild.id}_{item}', cost)
    asyli = discord.Embed(title="Создание предмета", description=f"Предмет `{item}` создан\nЕго цена: {cost}", color=0x0050ff)
    await ctx.send(embed=asyli)

@create_item.error
async def create_item_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(
            f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "
            f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(
            embed=discord.Embed(f"У вас недостаточно прав для использования данной "
                                    f"команды, требуемые права: "
                                    f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)
    
@client.slash_command(name="remove_item", description="Убрать придмет из магазина")
@commands.has_permissions(administrator = True)
async def remove_item(ctx, item):
    all_items = list(map(lambda a: a[0], list(filter(lambda a: f'_{item}' in a[0], db.all()))))
    for i in all_items:
        db.delete(i)
    asyli = discord.Embed(title="Удаление предмета", description=f"Предмет {item} удален из магазина", color=0x0050ff)
    await ctx.send(embed=asyli)

@remove_item.error
async def remove_item_error(interaction, error):
    if isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(f"Я не могу выполнить эту команду, потому что я не имею необходимых прав, а именно: "f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)
    elif isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message(embed=discord.Embed(f"У вас недостаточно прав для использования данной "f"команды, требуемые права: "f"`{' '.join(error.missing_permissions)}`"), ephemeral=True)

client.run("MTAxNDQ0OTk4NjE1NjYzODMzOA.G0jcMd.UuDXPa9ct8uuLHue4feC_zwcRxCVgOQ_C67P4M")
