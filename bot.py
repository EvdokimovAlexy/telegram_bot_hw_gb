from fractions import Fraction

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



value = ''
old_value = ''

choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [  # 1 row
            InlineKeyboardButton("7", callback_data="7"),
            InlineKeyboardButton(text="8", callback_data='8'),
            InlineKeyboardButton(text="9", callback_data='9'),
            InlineKeyboardButton(text="+/-", callback_data='+'),
            InlineKeyboardButton(text="<-", callback_data='<-'),
            InlineKeyboardButton(text="C", callback_data='C'),
            InlineKeyboardButton(text="", callback_data='no'),
        ],
        [  # 2 row
            InlineKeyboardButton(text="4", callback_data='4'),
            InlineKeyboardButton(text="5", callback_data='5'),
            InlineKeyboardButton(text="6", callback_data='6'),
            InlineKeyboardButton(text="/", callback_data='/'),
            InlineKeyboardButton(text="//", callback_data='//'),
            InlineKeyboardButton(text="%", callback_data='%'),
        ],
        [  # 3 row
            InlineKeyboardButton(text="1", callback_data='1'),
            InlineKeyboardButton(text="2", callback_data='2'),
            InlineKeyboardButton(text="3", callback_data='3'),
            InlineKeyboardButton(text="*", callback_data='*'),
            InlineKeyboardButton(text="-", callback_data='-'),
            InlineKeyboardButton(text="pow", callback_data='pow'),
        ],
        [  # 4 row
            InlineKeyboardButton(text="0", callback_data='0'),
            InlineKeyboardButton(text=",", callback_data=','),
            InlineKeyboardButton(text="+", callback_data='+'),
            InlineKeyboardButton(text="=", callback_data='='),
        ]
    ]
)

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
    kb.add(KeyboardButton('/calc'))
    return kb

def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/cancel'))

    return kb

def get_view_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/view'))

    return kb

def get_calc_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/calc'))

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
    await message.answer('Добро пожаловать в телефонную книгу - type /create\n type /view\n type /calc',
                         reply_markup=get_kb())

    # await edit_profile(chat_id=message.from_user.id)
@dp.message_handler(commands=['calc'])
async def cmd_calc(message: types.Message):
    global value
    if value == '':
        await bot.send_message(message.from_user.id, '2', reply_markup=choice)
    else:
        await bot.send_message(message.from_user.id, value, reply_markup=choice)


inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
@dp.message_handler(commands=['1'])
async def process_command_1(message: types.Message):
    await message.reply("Первая инлайн кнопка", reply_markup=inline_kb1)
@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')
@dp.message_handler(commands=['create'])
async def cmd_create(message: types.Message) -> None:
    await message.reply("Введите Вашу фамилию!",
                        reply_markup=get_cancel_kb())
    await ProfileStatesGroup.first_name.set()  # установили состояние имени

@dp.callback_query_handler(lambda callback_query: True)
async def callback_func(query):
    global value, old_value
    data1 = query.data

    if data1 == 'no':
        pass
    elif data1 == 'C':
        value = ''
    elif data1 == '=':
        value = str(eval(value))
    else:
        value += data1
    if value != old_value:
        if value == '':
            await bot.edit_message_text(text='0', reply_markup=choice)
        # else:
        #     await bot.edit_message_text(text=value, reply_markup=choice)
    old_value = value



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