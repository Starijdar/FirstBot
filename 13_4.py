from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio


api = "111"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    Age = State()
    Growth = State()
    Weight = State()


@dp.message_handler(commands=['start'])
async def start_messages(message):
    print(f'Wasup?')
    await message.answer('Привет! Я бот помогающий твоему здоровью.')

@dp.message_handler(text=['Calories', 'calories', 'калории', 'Калории'])
async def set_age(message):
    await message.answer('Введите свой возраст')
    await UserState.Age.set()

@dp.message_handler(state=UserState.Age)
async def set_height(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост')
    await UserState.Growth.set()

@dp.message_handler(state=UserState.Growth)
async def set_weight(message, state):
    await state.update_data(height=message.text)
    await message.answer('Введите свой вес')
    await UserState.Weight.set()

@dp.message_handler(state=UserState.Weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(f' Ваша норма: {int(data["weight"]) * 10 + int(data["height"]) * 6.25 - 5 * int(data["age"]) - 161}Ккал в день')
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)