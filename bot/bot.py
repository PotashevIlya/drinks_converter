import os
from dotenv import load_dotenv
from telebot import TeleBot, types
import requests
import json

load_dotenv()

URL = 'http://127.0.0.1:8000/convertation/'
data = {
    'source_name': None,
    'source_ml': None,
    'target_name': None
}

bot = TeleBot(token=os.getenv('TOKEN'))


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = message.chat.first_name
    keyboard = types.ReplyKeyboardMarkup()
    button_newcat = types.KeyboardButton('/convert')
    button_start = types.KeyboardButton('/start')
    keyboard.add(button_newcat)
    keyboard.add(button_start)

    bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}. Смотри, какие команды доступны',
        reply_markup=keyboard,
    )


@bot.message_handler(commands=['convert'])
def get_target_drinks(message):
    target_drinks_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    response = requests.get(url='http://127.0.0.1:8000/drink/')
    all_drinks = response.json()
    for drink in all_drinks:
        target_drinks_keyboard.add(drink['name'])
    target_drinks_keyboard.add('Без разницы!')
    msg = bot.send_message(
        message.from_user.id, 'Что хотите выпить?', reply_markup=target_drinks_keyboard)
    bot.register_next_step_handler(msg, get_source_drinks)


def get_source_drinks(message):
    if message.text != 'Без разницы!':
        data['target_name'] = message.text
    source_drinks_keyboard = types.ReplyKeyboardMarkup()
    response = requests.get(url='http://127.0.0.1:8000/drink/')
    all_drinks = response.json()
    for drink in all_drinks:
        if drink['name'] == message.text:
            continue
        source_drinks_keyboard.add(drink['name'])
    msg = bot.send_message(
        message.from_user.id, 'С каким напитком хотите сравнить?', reply_markup=source_drinks_keyboard)
    bot.register_next_step_handler(msg, get_source_ml)


def get_source_ml(message):
    data['source_name'] = message.text
    msg = bot.send_message(message.from_user.id, 'Укажите объем (мл):')
    bot.register_next_step_handler(msg, get_result)


def get_result(message):
    data['source_ml'] = message.text
    response = requests.post(url=URL, data=json.dumps(data))
    results = response.json()
    target = data.get('target_name')
    results_list = []
    results_str = '{name} - {ml} мл.'
    if isinstance(results, list):
        for result in results:
            results_list.append(results_str.format(
                name=result['target_name'], ml=result['target_ml']))
        pattern = [
            'Результат конвертации:',
            f'Ваш образец: {data["source_name"]} в объеме {data["source_ml"]} мл.',
            'Вам без разницы, что пить, поэтому ваши опции таковы:',
            *results_list
        ]
        bot.send_message(message.from_user.id, '\n'.join(pattern))
    else:
        pattern = [
            'Результат конвертации:',
            f'Ваш образец: {data["source_name"]} в объеме {data["source_ml"]} мл.',
            f'Вы хотите выпить {target}',
            f'Вам нужно выпить {results["target_ml"]} мл.'
        ]
        bot.send_message(message.from_user.id, '\n'.join(pattern))
    data['source_name'] = None
    data['source_ml'] = None
    data['target_name'] = None
    results_list.clear()


bot.polling()
