from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = "111"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def start_messages(message):
    print(f'Wasup?')
    await message.answer('Привет! Я бот помогающий твоему здоровью.')

@dp.message_handler()
async def all_messages(message):
    print(f'Другое сообщение')
    await message.answer(f"Введите команду /start, чтобы начать общение")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)