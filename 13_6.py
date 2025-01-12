from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


api = "111"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Расчитать')
kb.add(button1)
kb.insert(button2)

ikb = InlineKeyboardMarkup(inline_keyboard=[[ InlineKeyboardButton(text='Расчитать', callback_data='calories') ],
                           [
                               InlineKeyboardButton(text='Информация', callback_data='info'),
                           InlineKeyboardButton(text='Формула', callback_data='formula')
                           ]
                        ])


class UserState(StatesGroup):
    Age = State()
    Growth = State()
    Weight = State()


@dp.message_handler(commands=['start'])
async def start_messages(message):
    print(f'Wasup?', message)
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = ikb)

@dp.message_handler(text=['Информация', 'info'])
async def infooo(message):
    await message.answer('Информация о боте')

@dp.callback_query_handler(text='info')
async def infooo1(call):
    await call.message.answer('Информация о боте')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await call.answer()
    await UserState.Age.set()

@dp.message_handler(state=UserState.Age)
async def set_height(message, state):

    if not message.text.isdigit():
        print(message.content_type)
        await message.answer('цыферы тут нада')
        return
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост')
    await UserState.Growth.set()


@dp.message_handler(state=UserState.Growth)
async def set_weight(message, state):
    if not message.text.isdigit():
        print(message.content_type)
        await message.answer('цыферы тут нада')
        return
    await state.update_data(height=message.text)
    await message.answer('Введите свой вес')
    await UserState.Weight.set()


@dp.message_handler(state=UserState.Weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    try:
        await message.answer(f' Ваша норма: {int(data["weight"]) * 10 + int(data["height"]) * 6.25 - 5 * int(data["age"]) - 161} Ккал в день')
    except ValueError as err:
        await message.answer('Всё не то емаё')
    finally:
        await state.finish()


@dp.callback_query_handler(text='formula')
async def bringf(message):
    await message.message.answer(f'10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await message.answer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
