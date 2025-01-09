from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio


api = "7491997737:AAFCPUQqN6VdkVtCQ5cfSIYhx5lBuocCsrA"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Расчитать')
kb.add(button1)
kb.insert(button2)


class UserState(StatesGroup):
    Age = State()
    Growth = State()
    Weight = State()


@dp.message_handler(commands=['start'])
async def start_messages(message):
    print(f'Wasup?')
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler(text=['Информация'])
async def infooo(message):
    await message.answer('Информация о боте')


@dp.message_handler(text=['Calories', 'calories', 'калории', 'Калории', 'Расчитать'])
async def set_age(message):
    await message.answer('Введите свой возраст')
    await UserState.Age.set()

@dp.message_handler(state=UserState.Age)
async def set_height(message, state):
    try:
        if not isinstance(message, int):
            raise ValueError
        await message.answer('Введите свой рост')
        await UserState.Growth.set()
    except ValueError:
        await message.answer('цыферы тут нада')
        await state.finish()


@dp.message_handler(state=UserState.Growth)
async def set_weight(message, state):
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

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
