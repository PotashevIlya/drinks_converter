import os

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message
import aiohttp
import asyncio
from dotenv import load_dotenv


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



async def get_keyboard(target=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(ALL_DRINKS_URL) as response:
            all_drinks = await response.json()
            kb_list = [[KeyboardButton(text=drink['name'])] for drink in all_drinks if drink['name'] != target]
            if not target:
                kb_list.append([KeyboardButton(text='Без разницы!')])
            return ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)


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

@router.message(ConvertationProcess.choosing_target_drink)
async def target_drink_chosen(message:Message, state: FSMContext):
    if message.text == 'Без разницы!':
        await state.update_data(target_name=None)
    else:
        await state.update_data(target_name=message.text)
    await message.answer('Выберите, с каким напитком хотите сравнить:', reply_markup=get_keyboard(target=message.text))
    await state.set_state(ConvertationProcess.choosing_source_drink)




async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
