import discord
from discord.ext import commands
from pymorphy2 import MorphAnalyzer
import re
from collections import Counter
import matplotlib.pyplot as plt

morph = MorphAnalyzer()
client = commands.Bot(command_prefix='!')


@client.event
async def on_connect():
    print('Подключение к серверам Discord...')


@client.event
async def on_disconnect():
    print('Переподключение...')


@client.event
async def on_ready():
    print('Бот начал работу')


@client.command()
async def get_info(ctx):
    """Отправляет статистику использованных слов"""
    # Описание комманды
    morph_dict = {'NOUN': 0, 'NPRO': 0, 'VERB': 0, 'ADJF': 0, 'ADVB': 0, 'PREP': 0, 'CONJ': 0}
    # Словарь с тегами
    messages_data = []
    # Список русских слов
    async for message in discord.TextChannel.history(ctx, limit=None):
        if message.author != client.user and not message.content.startswith('!'):
            messages_data.append(message.content)
    # Если сообщение не от бота и не является командой, то добавляем
    messages_data = list(filter(lambda x: x != '',
                                re.sub(r"[^А-Яа-яЁё ]*", '',
                                       re.sub(r"[.,/+\"\'!:;]", ' ', ' '.join(messages_data))).split(' ')))
    # Убираем знаки препинания, оставляем только слова из русских букв)
    data = Counter(map(lambda x: morph.parse(x)[0].tag.POS, messages_data))
    # Объект типа Counter {Тег : кол-во слов}
    for i in data:
        if i in morph_dict:
            morph_dict[i] += data[i]
    # Обновляем словарь с тегами
    data, x = morph_dict.values(), range(7)
    # Кол-ва слов каждого типа, 7 столбцов
    fig, ax = plt.subplots()
    # Не понял что это, но без него не работает))
    plt.bar(x, data)
    # Создаем график типа bar
    plt.xticks(x, ('Сущ', 'Мест', 'Глаг', 'Прил', 'Нареч', 'Пред', 'Союз'))
    # Подписываем столбцы
    plt.savefig('info.jpg')
    # Сохраняем график
    await ctx.send('Держи, хорошего дня:3', file=discord.File('info.jpg'))
    # Отправляем сообщение


client.run('INSERT_TOKEN')
# Запуск бота)
