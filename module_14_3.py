from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.types.input_file import InputFile

# import foto as ft
# from PIL import image
import asyncio

api = '7214348790:AAHLRzW5NENdHcnLY9znrVIDC--6bsuUrJo'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.row(button, button2, button3)

kb2 = InlineKeyboardMarkup(resize_keyboard=True)
b1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
b2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb2.add(b1, b2)

kb_ph = InlineKeyboardMarkup(resize_keyboard=True)
b1_p = InlineKeyboardButton(text='Продукт 1', callback_data='product_buying')
b2_p = InlineKeyboardButton(text='Продукт 2', callback_data='product_buying')
b3_p = InlineKeyboardButton(text='Продукт 3', callback_data='product_buying')
b4_p = InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
kb_ph.insert(b1_p)
kb_ph.insert(b2_p)
kb_ph.insert(b3_p)
kb_ph.insert(b4_p)


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    with open('1.png', 'rb') as img:
        await message.answer_photo(img, f'Название:Product 1 | Описание:описание 1 | Цена:100')
    with open('2.png', 'rb') as img:
        await message.answer_photo(img, f'Название:Product 2 | Описание:описание 2 | Цена:200')
    with open('3.png', 'rb') as img:
        await message.answer_photo(img, f'Название:Product 3 | Описание:описание 3 | Цена:300')
    with open('4.png', 'rb') as img:
        await message.answer_photo(img, f'Название:Product 4 | Описание:описание 4 | Цена:400')

    await message.answer('Выберите продукт для покупки: ', reply_markup=kb_ph)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb2)


@dp.callback_query_handler(text=['product_buying'])
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(f'10 x вес(кг) + 6,25 х рост(см) - 5 х возраст(лет) + 5 - для мужчин;\n'
                              f'10 x вес(кг) + 6,25 х рост(см) - 5 х возраст(лет) - 161 - для женщин')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result_m = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    result_w = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
    await message.answer(f'Ваша норма калорий в сутки:\n'
                         f' {result_m} - для мужчин\n'
                         f' {result_w} - для женщин')
    await UserState.weight.set()
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
