import os
from dotenv import load_dotenv
from copy import deepcopy
from telebot import TeleBot, types
import requests
import json

load_dotenv()

CONVERTATION_URL = 'http://127.0.0.1:8000/convertation/'
DRINKS_URL = 'http://127.0.0.1:8000/drink/'
DATA = {
    'source_name': None,
    'source_ml': None,
    'target_name': None
}

bot = TeleBot(token=os.getenv('TOKEN'))


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = message.chat.first_name
    wake_up_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_convert = types.KeyboardButton('/convert')
    wake_up_keyboard.add(button_convert)

    bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}. Для конвертации нажми на команду',
        reply_markup=wake_up_keyboard,
    )


@bot.message_handler(commands=['convert'])
def get_target_drinks(message):
    input_data = deepcopy(DATA)
    target_drinks_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    response = requests.get(url=DRINKS_URL)
    all_drinks = response.json()
    for drink in all_drinks:
        target_drinks_keyboard.add(drink['name'])
    target_drinks_keyboard.add('Без разницы!')
    msg = bot.send_message(
        message.from_user.id,
        'Что хотите выпить?',
        reply_markup=target_drinks_keyboard
    )
    bot.register_next_step_handler(msg, get_source_drinks, input_data)


def get_source_drinks(message, input_data):
    if message.text != 'Без разницы!':
        input_data['target_name'] = message.text
    source_drinks_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    response = requests.get(url=DRINKS_URL)
    all_drinks = response.json()
    for drink in all_drinks:
        if drink['name'] == message.text:
            continue
        source_drinks_keyboard.add(drink['name'])
    msg = bot.send_message(
        message.from_user.id,
        'С каким напитком хотите сравнить?',
        reply_markup=source_drinks_keyboard
    )
    bot.register_next_step_handler(msg, get_source_ml, input_data)


def get_source_ml(message, input_data):
    input_data['source_name'] = message.text
    msg = bot.send_message(message.from_user.id, 'Укажите объем (мл):')
    bot.register_next_step_handler(msg, get_result, input_data)


def get_result(message, input_data):
    input_data['source_ml'] = message.text
    response = requests.post(url=CONVERTATION_URL, data=json.dumps(input_data))
    results = response.json()
    target = input_data.get('target_name')
    results_list = []
    results_str = '{name} - {ml} мл.'
    if isinstance(results, list):
        for result in results:
            results_list.append(results_str.format(
                name=result['target_name'],
                ml=result['target_ml']
            )
            )
        pattern = [
            'Результат конвертации:',
            f'Ваш образец: {input_data["source_name"]} в объеме {input_data["source_ml"]} мл.',
            'Вам без разницы, что пить, поэтому ваши опции таковы:',
            *results_list
        ]
        bot.send_message(message.from_user.id, '\n'.join(pattern))
    else:
        pattern = [
            'Результат конвертации:',
            f'Ваш образец: {input_data["source_name"]} в объеме {input_data["source_ml"]} мл.',
            f'Вы хотите выпить {target}',
            f'Вам нужно выпить {results["target_ml"]} мл.'
        ]
        bot.send_message(message.from_user.id, '\n'.join(pattern))
    del input_data
    results_list.clear()


def main():
    bot.polling(non_stop=True)


if __name__ == '__main__':
    main()
