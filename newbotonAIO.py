import csv
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from testAPIparsing import exchanger_currency
from text import text_start
from database import Database

storage = MemoryStorage()
bot = Bot (token = '')
dp = Dispatcher(bot, storage=storage)


keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add('Курс валют', 'Админ панель')
keyboard.add('Тех.поддержка')
keyboard.add('Рассылка')

keyboard_url = InlineKeyboardMarkup()
instagram_url = InlineKeyboardButton(text='Инстаграм', url = 'https://instagram.com/altynai.sunn?igshid=MzRlODBiNWFlZA==')
telegram_url = InlineKeyboardButton(text='Телеграм', url = 'https://t.me/AliSon771')
keyboard_url.add(instagram_url, telegram_url)

list_1 = [573015206, 1008889358, 5949761485, 5647517221, 5873445472, 5736318762]

# @bot.message_handler(commands=['start'])
# def hello_bot(message):
#     print(message.from_user.id)
#     bot.reply_to(message, f'Hi! {message.from_user.first_name} :)')

# @bot.message_handler(commands=['start', 'help'])
# def hello_bot(message):
#     user_id = message.from_user.id
#     first_name = message.from_user.first_name
#     last_name = message.from_user.last_name
#     print(f'id: {user_id}-----ник: {first_name}-----фамилия: {last_name}\n')
#     bot.reply_to(message, f'Привет, {message.from_user.first_name}!')
#     with open('database.txt', 'a') as file:
#         file.write(f'id: {user_id}-----ник: {first_name}-----фамилия: {last_name}\n')



# @bot.message_handler(commands=['start', 'help'])
# def hello_bot(message):
    # with open('database.txt', 'a') as file:
    #     file.write(f'{message.from_user.id}\n')
    # bot.send_message(message.from_user.id, text=text_start, reply_markup=keyboard)

    # ВАРИАНТ ДОБАВЛЕНИЯ В CSV-ФАЙЛ. МОЙ ВАРИАНТ. ПРОСТО ЗАПИСЬ.
    # with open('user_ids.csv', 'a', newline='', encoding = 'utf-8') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow([message.from_user.id, message.from_user.first_name])
    # bot.send_message(message.from_user.id, text=text_start, reply_markup=keyboard)

# ВАРИАНТ ДОБАВЛЕНИЯ В CSV-ФАЙЛ. ВАРИАНТ ЗАПИСИ ТОЛЬКО НОВЫХ ПОЛЬЗОВАТЕЛЕЙ.
# @bot.message_handler(commands=['start','help', '123'])
# def hello_bot(message):
#     with open('IDs.csv','r', newline='', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         user_id = [str(message.from_user.id),str(message.from_user.first_name)]
#         check_user =  list(reader)
#         if  user_id not in check_user:
#             with open('IDs.csv','a') as file:
#                 writer = csv.writer(file)
#                 writer.writerow([message.from_user.id, message.from_user.first_name])
#                 bot.send_message(message.from_user.id, text=text_start, reply_markup=keyboard)
#         else:
#             bot.send_message(message.from_user.id, text='Привет ты есть в базе', reply_markup=keyboard)

################ КОД СТАРТ - ВАРИАНТ АТОША

# @bot.message_handler(commands=['start','help'])
# def hello_bot(message):
#     with open('user_ids.csv','r', newline='', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         if [str(message.from_user.id), message.from_user.first_name] not in list(reader):
#             with open('user_ids.csv','a', newline='', encoding='utf-8') as file:
#                 writer = csv.writer(file)
#                 writer.writerow([message.from_user.id, message.from_user.first_name])
#     print(message.from_user.id,message.from_user.first_name)
#     bot.send_message(message.from_user.id, text=text_start, reply_markup=keyboard)


# ВАРИАНТ ДОБАВЛЕНИЯ В БАЗ ДАННЫХ В БОТА.
@dp.message_handler(commands=['start','help', '123'])
async def hello_bot(message: Message):
    db = Database()
    db.connect()
    db.create_user_table()
    first_name = message.from_user.first_name
    user_id = message.from_user.id
    check = db.check_user(user_id)
    if check:
        await bot.send_message(message.from_user.id, text='Привет, ты есть в базе', reply_markup=keyboard)
    else:
        db.insert_user(first_name, user_id)
        await bot.send_message(message.from_user.id, text='Привет, ты прошел регистрацию', reply_markup=keyboard)
    db.close()
    

@dp.message_handler(commands=['info'])
async def info_bot(message: Message):
    class MessageList(StatesGroup):
        text = State()

    db = Database()
    db.connect()
    user_list = db.mailing_message()
    if message.from_user.id == 346706198:
        await MessageList.text.set()
        await message.answer('Введите текст для рассылки')

        @dp.message_handler(state=MessageList.text)
        async def mail_text(message:Message, state: FSMContext):
            async with state.proxy() as data:
                data['text'] = message.text
                text = data['text']

            for item in user_list:
                try:
                    await bot.send_message(chat_id = item[0], text=text)
                    await state.finish()
                except Exception:
                    pass
            await bot.send_message(message.from_user.id, text='Рассылка успешно отправлена', reply_markup=keyboard)

    elif message.from_user.id != 346706198:
        await message.reply ('Вы не админ, шалость не удалась)')
    db.close()


# @bot.message_handler(commands=['admin'])
# def admin_bot(message):
#     if message.from_user.id == 346706198:
#         bot.reply_to(message, 'Привет, админка!')
#         with open('database.txt', 'r') as file:
#             text = file.read()
#             bot.reply_to(message, f'Вот список всех посетителей Бла-Бла бота: \n\n{text}')
#         with open('database.txt','r') as file:
#             display_ID = file.readlines()
#         for ids in display_ID:
#             bot.send_message(chat_id=ids, text='Рассылка только для тебя')
#         bot.send_message(message.from_user.id, text='Рассылка успешно отправлена')      
        
#     else:
#         bot.reply_to(message, 'Вы не админ, список пользователей Бла-Бла бота недоступен')


############# КНОПКА АДМИН - РАБОТА С БАЗАМИ ДАННЫХ


@dp.message_handler(commands=['admin'])
async def admin_bot(message: Message):
    db = Database()
    db.connect()
    all_users = (db.all_users())
    
    if message.from_user.id == 346706198:
        await message.reply ('Привет, админка!')
        text = 'Вск пользователи бота:\n'
        for users in all_users:
            text += f'{users[0]}\n'
        await bot.send_message(message.from_user.id, text = text)
            
    else:
        await message.reply('Вы не админ, список пользователей Бла-Бла бота недоступен')



# @bot.message_handler(content_types='photo')
# def message_photo(message):
#     photo = open('123.jpg', 'rb')
#     bot.send_photo(message.from_user.id, photo, caption='Привет! Я - фото-котик, реагирую на любое фото')
#     photo.close()


@dp.message_handler(content_types='text')
async def message_text(message: Message):
    first_name = message.from_user.first_name
    msg = message.text
    with open('msg_text.txt', 'a') as file:
        file.write(f'От пользователя: {first_name} - Сообщение: {msg}\n')   

    if message.text == 'Тех.поддержка':
        await bot.send_message(message.from_user.id, text='Связаться с отделом заботы можно по ссылке\n@AliSon771', reply_markup=keyboard_url)

    elif message.text == 'Рассылка':
        await info_bot(message)

    elif message.text == 'Админ панель':
        await admin_bot(message)

    elif message.text == 'Курс валют':
        currency = exchanger_currency()
        currency_list = []
        for key, value in currency.items():
            result = f'{key} - {value}'
            currency_list.append(result)
        text = '\n'.join(currency_list)
        await bot.send_message(message.from_user.id, text=f'Курсы валют\n\n{text}')
    else:
        await bot.send_message(message.from_user.id, text='Вы имеете право хранить молчание. Все, что вы скажете может быть использовано против вас.')

# @bot.message_handler() # пустой хэндлер всегда должен быть внизу.
# def hello_user(message):
#     if message.text.lower() == 'hello':
#         bot.reply_to(message, 'Hello!')

#     elif message.text.lower() == 'how r u':
#         bot.reply_to(message, 'Could be better, what about you?')


# @bot.message_handler()
# def echo_message(message):
#     bot.send_message(chat_id = message.from_user.id, text = message.text)


if __name__ == '__main__': #
    executor.start_polling(dp, skip_updates=True)