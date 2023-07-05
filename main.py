from aiogram import Bot, Dispatcher
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token='')
dp = Dispatcher(bot, storage=storage)


keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add('Регистрация')


@dp.message_handler(commands='start')
async def start_command(message: Message):
    await bot.send_message(message.from_user.id, 'Привет! Чтобы пользоваться ботом,\
                            нужно пройти регистрацию. Для этого нажми на кнопку "Регистрация"', reply_markup=keyboard)


@dp.message_handler(text='Регистрация')
async def registration(message: Message):
    # МАШИНА СОСТОЯНИЙ - AIOGRAM
    class Registration(StatesGroup):
        name = State()
        age = State()
        phone = State()
        about = State()
        # ВНУТРИ ТЕЛА КЛАССА НИЧЕГО НЕ ДОЛЖНО ХРАНИТЬСЯ, ТОЛЬКО ВЫЗЫВАЕМ ФУНКЦИИ
    # ОСТАЛЬНОЕ ПИШЕМ НА ОДНОМ УРОВНЕ С КЛАССОМ
    await Registration.name.set()
    await message.answer('Введите ваше имя')

    @dp.message_handler(state=Registration.name)
    async def name_user(message: Message, state: FSMContext):
        async with state.proxy() as data:
            data['name'] = message.text
            await message.answer('Введите ваш возраст')
            await Registration.next()

    @dp.message_handler(state=Registration.age)
    async def age_user(message: Message, state: FSMContext):
        async with state.proxy() as data:
            data['age'] = message.text
            await message.answer('Введите ваш номер телефона в формате (+кодстраны)номер')
            await Registration.next()

    @dp.message_handler(state=Registration.phone)
    async def phone_user(message: Message, state: FSMContext):
        async with state.proxy() as data:
            data['phone'] = message.text
            await message.answer('Расскажи немного о себе')
            await Registration.next()

    @dp.message_handler(state=Registration.about)
    async def about_user(message: Message, state: FSMContext):
        async with state.proxy() as data:
            data['about'] = message.text
            name = data['name']
            age = data['age']
            phone = data['phone']
            about = data['about']
            text = f'Ваши данные:\nИмя:{name}\nВозраст:{age}\nТелефон:{phone}\nО себе:{about}'

            await bot.send_message(message.from_user.id, text=f'Регистрация прошла успешно!{text}')
            await state.finish()
    


if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True)
