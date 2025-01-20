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

kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Расчитать'),
        KeyboardButton(text='Информация')
     ], [
        KeyboardButton(text='Купить')
    ]
], resize_keyboard=True)


catalog_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Product1', callback_data='product_buying'),
        InlineKeyboardButton(text='Product2', callback_data='product_buying'),
        InlineKeyboardButton(text='Product3', callback_data='product_buying'),
        InlineKeyboardButton(text='Product4', callback_data='product_buying')
    ]
])


class UserState(StatesGroup):
    Age = State()
    Growth = State()
    Weight = State()


@dp.message_handler(commands=['start'])
async def start_messages(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler(text=['Информация', 'info'])
async def infooo(message):
    await message.answer('Информация о боте')

'''
Блок подсчета калорий
'''
@dp.message_handler(text='Расчитать')
async def set_age(call):
    await call.answer('Введите свой возраст')
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

'''
Блок магазина
'''


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(1, 5):
        await message.answer(f'Product{i} | Описание{i} | Цена{i * 1000}')
        with open(f'products/{i}.jpg', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки' , reply_markup=catalog_kb)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
