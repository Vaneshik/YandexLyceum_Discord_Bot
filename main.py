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
    ax.set_title('Количество слов по частям речи:')
    plt.savefig('info.png')
    # Сохраняем график

    for i in range(len(messages_data)):
        messages_data[i] = (morph.parse(messages_data[i])[0]).normal_form
    # Приводим слова в исходную форму
    data = {}
    for i in Counter(messages_data):
        if "NPRO" not in morph.parse(i)[0].tag and "PREP" not in morph.parse(i)[0].tag \
                and "CONJ" not in morph.parse(i)[0].tag:
            data[i] = messages_data.count(i)
    # Формируем словарь, ключами которого являются слова, а значениями - количество их повторений
    lst = list(data.items())
    lst.sort(key=lambda i: i[1], reverse=True)
    # Создаём из словаря список кортежей вида "(слово, кол-во повторений)" для того, чтобы его можно было отсортировать.
    comment = morph.parse('повторение')[0]
    await ctx.send(f'Приуэт! Топ-5 слов на этом канале: \n 1.) "{lst[0][0]}", {lst[0][1]} {comment.make_agree_with_number(lst[0][1]).word} \n'
                   f'2.) "{lst[1][0]}", {lst[1][1]} {comment.make_agree_with_number(lst[1][1]).word} \n 3.) "{lst[2][0]}", {lst[2][1]} {comment.make_agree_with_number(lst[2][1]).word} \n'
                   f'4.) "{lst[3][0]}", {lst[3][1]} {comment.make_agree_with_number(lst[3][1]).word} \n 5.) "{lst[4][0]}", {lst[4][1]} {comment.make_agree_with_number(lst[4][1]).word} \n',
                   file=discord.File('info.png'))
    # Приводим слова в соответствие с чилительными и отправляем

client.run('INSERT_TOKEN')
# Запуск бота)
