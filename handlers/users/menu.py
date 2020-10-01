from loader import dp
from aiogram import types
from timetable import create_message


@dp.message_handler(commands=['start', 'menu'])
async def send_menu(message: types.Message):
    await message.answer(text=create_message())