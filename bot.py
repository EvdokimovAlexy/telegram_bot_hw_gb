from aiogram import types, executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, message
from data_base import sqlite
from data_base.sqlite import db_start, edit_profile
from aiogram.utils.callback_data import CallbackData
async def on_startup(_):
    await db_start()

profile_cb = CallbackData('profile', 'id', 'action')
storage = MemoryStorage()
bot = Bot(token='5916611210:AAEaM28c0Z6rZIjzmk6pDwWhb1Jks74ZMso')
dp = Dispatcher(bot,
                storage=storage)



class ProfileStatesGroup(StatesGroup):

    first_name = State()
    name = State()
    number = State()
    description = State()


# def get_edit_ikb(product_id: int) -> InlineKeyboardMarkup:
#     ikb = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton('Редактировать контакт', callback_data=profile_cb.new(profile_id, 'edit'))],
#         [InlineKeyboardButton('Удалить контакт', callback_data=profile_cb.new(product_id, 'delete'))],
#     ])   # кнопки в разработке

    # return ikb

def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/create'))

    return kb

def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/cancel'))

    return kb

def get_view_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/view'))

    return kb

# def get_products_ikb() -> InlineKeyboardMarkup:
#     ikb = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton('Просмотр всех контактов', callback_data='get_all_products')],
#         [InlineKeyboardButton('Добавить новый контакт', callback_data='add_new_product')],
#     ])   # Клавиатура в разработке

    # return ikb


@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return

    await state.finish()
    await message.reply('Вы прервали создание контакта!',
                        reply_markup=get_kb())


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.answer('Добро пожаловать в телефонную книгу - type /create\n /view',
                         reply_markup=get_kb())

    await edit_profile(chat_id=message.from_user.id)


@dp.message_handler(commands=['create'])
async def cmd_create(message: types.Message) -> None:
    await message.reply("Введите Вашу фамилию!",
                        reply_markup=get_cancel_kb())
    await ProfileStatesGroup.first_name.set()  # установили состояние имени


@dp.message_handler(state=ProfileStatesGroup.first_name)
async def load_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['first_name'] = message.text

    await message.reply('Введите Ваше имя!')
    await ProfileStatesGroup.next()

@dp.message_handler(state=ProfileStatesGroup.name)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply('Введите Ваш номер телефона')
    await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.number)
async def load_age(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['number'] = message.text

    await message.reply('Введите описание контакта!')
    await ProfileStatesGroup.next()


@dp.message_handler(state=ProfileStatesGroup.description)
async def load_desc(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['description'] = message.text
        # await bot.send_photo(chat_id=message.from_user.id,
        #                      # first_name=data['first_name'],
        #                      caption=f"{data['name']}, {data['name']}\n{data['description']}")

    await edit_profile(state)
    await message.reply('Ваш контакт создан!')
    await state.finish()



@dp.message_handler(commands=['view'])
async def export(message: types.Message):
    read = await sqlite.get_all_products()
    await bot.send_message(message.chat.id, read)

if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)