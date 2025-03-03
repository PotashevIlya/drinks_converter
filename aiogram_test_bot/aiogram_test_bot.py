import os

from aiogram import Bot, Dispatcher, Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message
import aiohttp
import asyncio
from dotenv import load_dotenv
from copy import deepcopy


load_dotenv()

BOT_TOKEN = os.getenv('TOKEN')
ALL_DRINKS_URL = 'http://127.0.0.1:8000/drink/'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()


class ConvertationProcess(StatesGroup):
    choosing_target_drink = State()
    choosing_source_drink = State()
    choosing_source_drink_ml = State()


async def get_available_drink_names() -> list[str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(ALL_DRINKS_URL) as response:
            available_drinks = [drink['name'] for drink in await response.json()]
            available_drinks.append('Без разницы!')
            return available_drinks

available_drinks = asyncio.run(get_available_drink_names())


async def get_keyboard(target=None):
    all_drinks = deepcopy(available_drinks)
    if target:
        all_drinks.remove(target)
        if target != 'Без разницы!':
            all_drinks.remove('Без разницы!')
    kb_list = [[KeyboardButton(text=name)] for name in all_drinks]
    return ReplyKeyboardMarkup(keyboard=kb_list, one_time_keyboard=True)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f'Привет, {message.chat.first_name}!\n'
        f'Чтобы начать конвертацию кликай сюда - /convertation'
    )


@router.message(StateFilter(None), Command('convertation'))
async def cmd_convertation(message: Message, state: FSMContext):
    await message.answer('Выберите, что хотите выпить:', reply_markup=await get_keyboard())
    await state.set_state(ConvertationProcess.choosing_target_drink)


@router.message(
    ConvertationProcess.choosing_target_drink,
    F.text.in_(available_drinks)
)
async def target_drink_chosen(message: Message, state: FSMContext):
    if message.text == 'Без разницы!':
        await state.update_data(target_name=None)
    else:
        await state.update_data(target_name=message.text)
    await message.answer('Выберите, с каким напитком хотите сравнить:', reply_markup=await get_keyboard(target=message.text))
    await state.set_state(ConvertationProcess.choosing_source_drink)


@router.message(ConvertationProcess.choosing_target_drink)
async def target_drink_chosen_incorrectly(message: Message):
    await message.answer(
        text=(
            f'Я не знаю напитка {message.text}\n'
            f'Пожалуйста, выберите вариант из списка ниже:'
        ),
        reply_markup=await get_keyboard()
    )


@router.message(
    ConvertationProcess.choosing_source_drink,
    F.text.in_(available_drinks)
)
async def source_drink_chosen(message: Message, state: FSMContext):
    await state.update_data(source_name=message.text)
    await message.answer('Укажите объём напитка-образца в мл:')
    await state.set_state(ConvertationProcess.choosing_source_drink_ml)


@router.message(ConvertationProcess.choosing_source_drink)
async def source_drink_chosen_incorrectly(message: Message, state: FSMContext):
    data = await state.get_data()
    target = data.get('target_name')
    if not target:
        target = 'Без разницы!'
    await message.answer(
        text=(
            f'Я не знаю напитка {message.text}\n'
            f'Пожалуйста, выберите вариант из списка ниже:'
        ),
        reply_markup=await get_keyboard(target=target)
    )


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
