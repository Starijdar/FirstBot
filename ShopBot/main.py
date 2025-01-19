import logging
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

from config import *
from keyboards import *
import texts

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(texts.start + f"{message.from_user.first_name}", reply_markup=start_kb)


@dp.message_handler(text=['О нас'])
async def price(message):
    await message.answer(texts.about, reply_markup=start_kb)


@dp.message_handler(text=['Стоимость'])
async def price(message):
    await message.answer('Что вас интересует?', reply_markup=catalog_kb)

@dp.message_handler(text=['Нажми для котика'])
async def kotiatki(message):
    i = random.randint(1, 4)
    with open(f'files/{i}.jpg', "rb") as img:
        await message.answer_photo(img, reply_markup=start_kb)


@dp.callback_query_handler(text='medium')
async def buy_m(call):
    await call.message.answer(texts.Mgame, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text='big')
async def buy_l(call):
    await call.message.answer(texts.Lgame, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text='xtral')
async def buy_xl(call):
    await call.message.answer(texts.XLgame, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text='other')
async def buy_other(call):
    await call.message.answer(texts.other, reply_markup=buy_kb)
    await call.answer()

@dp.callback_query_handler(text='back')
async def backbut(call):
    await call.message.answer('Что вас интересует?', reply_markup=catalog_kb)
    await call.answer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)